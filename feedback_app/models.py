from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Feedback(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class FeedbackReply(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name='replies')
    admin = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    message = models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply to {self.feedback.id}"