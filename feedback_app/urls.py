from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomePageView.as_view(),name="homepage"),
    path('register/',views.UserRegistrationView.as_view(),name="register"),
    path('login/',views.UserLoginView.as_view(),name="login"),
    path('logout/',views.UserLogoutView.as_view(),name="logout"),
    path('feedback_form',views.FeedbackFormView.as_view(),name="feedback_form"),
    path('feedback/submit',views.SubmitFeedbackView.as_view(),name="submit_feedback"),
    path('dashboard',views.AdminDashboardView.as_view(),name="admin_dashboard"), # admin dashboard panel url
    path('dashboard/feedback/<int:pk>/reply/',views.AdminFeedbackReplyView.as_view(),name="admin_feedback_reply"), # admin reply url
    path('my/feedback/',views.MyFeedbackView.as_view(),name="my_feedback"),  # regular user feedback list url
    path('update/feedback/<int:pk>/',views.EditFeedbackView.as_view(),name="edit_feedback"),
    path('delete/feedback/<int:pk>/',views.DeleteFeedbackView.as_view(),name="delete_feedback")
]