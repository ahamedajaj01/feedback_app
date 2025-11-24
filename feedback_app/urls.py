from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomePageView.as_view(),name="homepage"),
    path('register/',views.user_registration,name="register"),
    path('login/',views.login,name="login"),
    path('logout',views.logout,name="logout"),
    path('feedback_form',views.feedback_form,name="feedback_form"),
    path('feedback/submit',views.submit_feedback,name="submit_feedback"),
    path('dashboard',views.admin_dashboard,name="admin_dashboard"), # admin dashboard panel url
    path('dashboard/feedback/<int:pk>/reply/',views.admin_feedback_reply,name="admin_feedback_reply"), # admin reply url
    path('my/feedback/',views.my_feedback,name="my_feedback"),  # regular user feedback list url
    path('update/feedback/<int:pk>/',views.edit_feedback,name="edit_feedback"),
    path('delete/feedback/<int:pk>/',views.delete_feedback,name="delete_feedback")
]