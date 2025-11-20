from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import Registration,LoginForm, FeedbackForm
from .models import Feedback
from django.contrib import messages

# Create your views here.
def homepage(request):
     # If admin or staff → keep them in admin area
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
           return redirect("admin_dashboard")  
     # Normal users can see homepage
    return render(request,"homepage.html")

def user_registration(request):
    # If user already logged in → stop them
    if request.user.is_authenticated:
         if request.user.is_staff or request.user.is_superuser:
                       return redirect('admin_dashboard')
         return redirect('homepage')
         
    if request.method == "POST":
        form = Registration(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password']
            )
            return redirect('login')
    else:
        form = Registration()

    return render(request,"registration/registration.html",{"form":form})

def login(request):
     # If user already logged in → stop them
    if request.user.is_authenticated:
         if request.user.is_staff or request.user.is_superuser:
                       return redirect('admin_dashboard')
    
         return redirect("homepage")
    
     # If the form was submitted
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Check username + password
            user = authenticate(request,username = username, password=password)

            if user is not None:
                # Log the user in (creates session)
                auth_login(request,user)

                 # If the user is staff or superuser, send to the admin feedback page
                if user.is_staff or user.is_superuser:
                    return redirect('admin_dashboard')
                 # Otherwise send regular users to homepage
                return redirect('homepage')
            else:
                # Authentication failed
                form.add_error(None, "Invalid username or password")
    else:
        # Show empty form on GET
        form = LoginForm()
    
    return render(request,"login.html",{"form":form})

def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def feedback_form(request):
    return render(request,"feedback_form.html")


@login_required
def submit_feedback(request):

    # This view only handles form submission (POST request)
    if request.method == "POST":

        # Get form data from the page
        # request.POST.get("field_name", "default_value")
        # .strip() removes extra spaces
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message_text = request.POST.get("message", "").strip()

        # If the message is empty, do not save it
        if not message_text:
            messages.error(request, "Message cannot be empty")
            return redirect("feedback_form")   # Go back to form page

        # Save the feedback in the database
        Feedback.objects.create(
            name=name,
            email=email,
            message=message_text,
            user = request.user
        )

        # Show a success message on the form page
        messages.success(request, "Feedback submitted successfully.")

        # Redirect back to the same form page
        # This clears the form and avoids duplicate submissions
        return redirect('feedback_form')

    # If someone tries to access this view without POST (GET request),
    # just send them back to the form page.
    return redirect('feedback_form')

# admin dashboard
@login_required
def admin_dashboard(request):
    # Only allow admin users
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('homepage')
    feedbacks = Feedback.objects.all()
    return render(request,"admin_dashboard/dashboard.html",{"feedbacks":feedbacks})


@login_required
def my_feedback(request):
      # Block admin & staff accounts
    if request.user.is_staff or request.user.is_superuser:
        return redirect("admin_dashboard")  # or 'homepage' if you prefer
    
    # Only normal users reach this part
    feedback = Feedback.objects.filter(user=request.user).order_by('-created_at')
    return render(request,"my_feedback.html",{"feedback":feedback})

@login_required
def edit_feedback(request,pk):
    # Load the single Feedback object or return 404 if not found
     feedback = get_object_or_404(Feedback,pk=pk)

    # Security check: only the owner (user) can edit their feedback
    # If you store user in Feedback.user
     if feedback.user is None or feedback.user != request.user:
          # Not the owner: forbid access (or redirect with a message)
          messages.error(request,"You are not allowed to edit this feedback.")
          return redirect('my_feedback')
     
     if request.method == "POST":
           # Bind form to POST data and the instance we are editing
          form = FeedbackForm(request.POST,instance=feedback) # Populate form with submitted data and existing post instance
          if form.is_valid():
               form.save()
               messages.success(request, "Feedback updated successfully.")
               return redirect('my_feedback')
     else:
           form=FeedbackForm(instance=feedback)
     return render(request,'edit_feedback.html',{"form":form, "feedback":feedback})


@login_required
def delete_feedback(request,pk):
     feedback = get_object_or_404(Feedback,pk=pk)

    # Determine the default redirect target
    # - if the current user is staff (admin), default to admin dashboard
    # - otherwise default to the user's feedback list
     default_redirect = 'admin_dashboard' if request.user.is_staff else 'my_feedback'

     # Find where to redirect after delete (check POST, then GET)
     next_url_name = request.POST.get('next') or request.GET.get('next') or default_redirect

     # Security check:
    # - owner can delete
    # - staff can delete any feedback
     if not (request.user.is_staff or (feedback.user is not None and feedback.user == request.user)):
        # unauthorized: redirect back to safe place
        return redirect(default_redirect)

     if request.method == "POST":
          feedback.delete()
          return redirect(next_url_name)
     
     # show confirmation page; pass the 'next' so the form can send it back
     return render(request, "confirm_delete.html", {"feedback": feedback, "next":next_url_name})


         
