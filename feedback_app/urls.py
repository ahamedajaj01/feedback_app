from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.homepage,name="homepage"),
    path('register/',views.user_registration,name="register"),
    path('login/',views.login,name="login"),
    path('logout',views.logout,name="logout"),
    path('feedback_form',views.feedback_form,name="feedback_form"),
    path('feedback/submit',views.submit_feedback,name="submit_feedback"),
    path('users/feedback/list',views.admin_feedback_list,name="admin_feedback_list"),
    path('my/feedback/',views.my_feedback,name="my_feedback"),
    path('update/feedback/<int:pk>/',views.edit_feedback,name="edit_feedback"),
    path('delete/feedback/<int:pk>/',views.delete_feedback,name="delete_feedback")
]