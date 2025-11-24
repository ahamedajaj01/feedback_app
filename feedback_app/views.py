from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import TemplateView, FormView, ListView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .forms import Registration, FeedbackForm
from .models import Feedback, FeedbackReply
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

# Create your views here.
class HomePageView(TemplateView):
     template_name = "homepage.html"

     # This runs before any GET/POST handler.
     def dispatch(self, request, *args, **kwargs):
     # If admin or staff → keep them in admin area
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
           return redirect("admin_dashboard")  
        
        # Otherwise continue normally (show homepage)
        return super().dispatch(request,*args, **kwargs)


class UserRegistrationView(FormView):
     template_name="registration/registration.html"
     form_class = Registration
     success_url = "login/"

     # Runs before get/post → handle early redirects
     def dispatch(self,request,*args,**kwargs):
          # If user is logged in → do not let them access registration
           if request.user.is_authenticated:
                # staff/admin → go to admin dashboard
                if request.user.is_staff or request.user.is_superuser:
                     return redirect('admin_dashboard')
                # normal user → go to homepage
                return redirect('homepage')
           return super().dispatch(request,*args,**kwargs)
     
     # Called only when form is valid (POST)
     def form_valid(self,form):
          # Create user from cleaned form data
          User.objects.create_user(
                username=form.cleaned_data['username'],
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password']
          )
          return super().form_valid(form)


class UserLoginView(LoginView):
     template_name = "login.html"
     form_class = AuthenticationForm
     # If user already logged in → redirect them
     def dispatch(self,request,*args,**kwargs):
          if request.user.is_authenticated:
               if request.user.is_staff or request.user.is_superuser:
                    return redirect('admin_dashboard')
               # normal user → go to homepage
               return redirect('homepage')
          return super().dispatch(request,*args,**kwargs)
     
     # where to go after successful login
     def get_success_url(self):
          # Staff/admin → admin dashboard
          if self.request.user.is_staff or self.request.user.is_superuser:
               return reverse_lazy("admin_dashboard")
          return reverse_lazy('homepage')
                    

class UserLogoutView(LogoutView):
     next_page=reverse_lazy("login")


class FeedbackFormView(LoginRequiredMixin,TemplateView):
     template_name="feedback_form.html"


class SubmitFeedbackView(LoginRequiredMixin,View):
     # handle post submission
     def post(self,request,*args,**kwargs):
          # extract  fields from post
           # .strip() removes extra spaces
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message_text = request.POST.get("message", "").strip()

        # validate messages
        # If the message is empty, do not save it
        if not message_text:
             messages.error(request,"Messages cannot be empty")
             return redirect("feedback_form")  # Go back to form page
        
        # save feedback in db
        Feedback.objects.create(
             name=name,
            email=email,
            message=message_text,
            user = request.user
        )
         # Show a success message
        messages.success(request, "Feedback submitted successfully.")

        # Redirect back to the same form page
        # This clears the form and avoids duplicate submissions
        return redirect('feedback_form')
     
      # If someone tries to access this view without POST (GET request),
      # just send them back to the form page.
     def get(self,request,*args,**kwargs):
          return redirect("feedback_form")


# admin dashboard
class AdminDashboardView(LoginRequiredMixin,ListView):
     model = Feedback
     template_name = "admin_dashboard/dashboard.html"
     context_object_name = "feedbacks"

     # Only staff/superuser may access; others are redirected to homepage
     def dispatch(self,request,*args,**kwargs):
          if not(request.user.is_staff or request.user.is_superuser):
               return redirect("homepage")
          return super().dispatch(request,*args,**kwargs)
     
     # Build the queryset with search and date filters
     def get_queryset(self):
          # Start from the base queryset for Feedback
          qs = super().get_queryset()
          q = self.request.GET.get("q", "").strip()
          date_filter = self.request.GET.get("date", "").strip()
     
          # text search across name, email, message
          if q:
               qs = qs.filter(Q(name__icontains=q)|Q(email__icontains=q)|Q(message__icontains=q))

          # date filters: today / week
          now = timezone.now()
          local_now = timezone.localtime(now)
          start = local_now.replace(hour=0, minute=0, second=0, microsecond=0)
          if date_filter =="today":
               end = start + timedelta(days=1)
               qs = qs.filter(created_at__gte =start, created_at__lt=end) 
          elif date_filter == "week":
            since = now - timedelta(days=7)
            qs = qs.filter(created_at__gte=since)

          return qs.order_by("-created_at")
     
     # Add `request` to context so templates that reference request.GET still work
     def get_context_data(self,**kwargs):
          ctx = super().get_context_data(**kwargs)
          ctx["request"] = self.request
          return ctx


# admin feedback reply
class AdminFeedbackReplyView(LoginRequiredMixin,UserPassesTestMixin,View):
     template_name = "admin_dashboard/reply.html"

      # Allow only staff/admin users to reply
     def test_func(self):
           return self.request.user.is_staff or self.request.user.is_superuser
     
     # GET → show reply form
     def get(self,request,pk,*args,**kwargs):
     # Get the feedback or show 404 if not found
          feedback = get_object_or_404(Feedback,pk=pk)
          return render(request,self.template_name,{"feedback":feedback})
     
     # POST → save reply
     def post(self,request,pk,*args,**kwargs):
          feedback = get_object_or_404(Feedback,pk=pk)
          message = request.POST.get("message","").strip()

          # If message is empty, reload page ( or you can add error later)
          if not message:
               return redirect("admin_dashboard")
  
        # Save reply to database
          FeedbackReply.objects.create(
             feedback=feedback,
             admin=request.user,
             message=message,
          )
         # After saving, go back to dashboard or feedback list
          return redirect('admin_dashboard')


class MyFeedbackView(LoginRequiredMixin,ListView):
     model = Feedback
     template_name="my_feedback.html"
     context_object_name="feedback"   # your template expects "feedback" (a queryset)

      # Block admin & staff accounts
     def dispatch(self,request,*args,**kwargs):
          if request.user.is_staff or request.user.is_superuser:
               return redirect("admin_dashboard")
          return super().dispatch(request,*args,**kwargs)
     
     # Only show feedback that belongs to the current user, newest first
     def get_queryset(self):
          return Feedback.objects.filter(user=self.request.user).order_by("-created_at")


class EditFeedbackView(LoginRequiredMixin,UpdateView):
     model = Feedback
     form_class = FeedbackForm
     template_name = "edit_feedback.html"
     context_object_name="feedback"

      # Security: only allow the owner to edit
     def dispatch(self,request,*args,**kwargs):
          feedback = self.get_object()
          if feedback.user is None or feedback.user != request.user:
               return redirect("my_feedback")
          return super().dispatch(request,*args,**kwargs)
     
     # After saving, go back to user's feedback list
     def form_valid(self,form):
          messages.success(self.request,"Feedback updated successfully.")
          return super().form_valid(form)
     
     def get_success_url(self):
          return reverse_lazy("my_feedback")


class DeleteFeedbackView(LoginRequiredMixin,UserPassesTestMixin,View):
     """
    GET -> show confirmation template (confirm_delete.html)
    POST -> perform delete, then redirect to 'next' or sensible default.
    """
     # Only allow staff or the owner of the feedback to delete
     def test_func(self):
          # allow staff OR owner
          pk = self.kwargs.get("pk")
          feedback = get_object_or_404(Feedback,pk=pk)
          # owner allowed if feedback.user exists and equals current user
          is_owner = feedback.user is not None and feedback.user == self.request.user
          return self.request.user.is_staff or is_owner
     
     # Determine default redirect if 'next' not provided
     def get_default_redirect(self):
        # staff users go to admin dashboard by default, others to their feedback list
        return "admin_dashboard" if self.request.user.is_staff else "my_feedback"
     
     # Get 'next' parameter from POST or GET data
     def get_next_name(self):
        # prefer POST, then GET, else fallback
        return self.request.POST.get("next") or self.request.GET.get("next") or self.get_default_redirect()
     
     # Show confirmation template
     def get(self, request, pk, *args, **kwargs):
        # show confirmation. include 'next' so template form can resend it
        feedback = get_object_or_404(Feedback, pk=pk)
        next_name = self.get_next_name()
        return render(request, "confirm_delete.html", {"feedback": feedback, "next": next_name})
     
     # Handle deletion
     def post(self, request, pk, *args, **kwargs):
        # perform final permission check and delete
        feedback = get_object_or_404(Feedback, pk=pk)

        # double-check permission (UserPassesTestMixin should already enforce this,
        # but it's safe to keep an explicit guard)
        if not (request.user.is_staff or (feedback.user is not None and feedback.user == request.user)):
            return redirect(self.get_default_redirect())

        next_name = self.get_next_name()
        # Delete and redirect
        feedback.delete()
        # if next_name looks like a URL name, reverse it; if it's already a URL path, you can detect and use directly.
        # Here we assume callers pass a URL name (as in your FBV). Use reverse() to resolve name->path.
        try:
            return redirect(reverse_lazy(next_name))
        except Exception:
            # fallback: if reversing fails, redirect by name directly (redirect handles names too)
            return redirect(next_name)



