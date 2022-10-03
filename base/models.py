from django.db import models
from django.contrib.auth.models import AbstractUser


# custom user model
class User(AbstractUser):
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(unique=True,null=True)
    avatar = models.ImageField(default="default-user.png",null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


# Create your models here.
class Password(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='account_user')
    app_username = models.CharField(max_length=100)
    app_password = models.CharField(max_length=100)
    app_name = models.CharField(max_length=100)
    notes = models.CharField(max_length=100,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.app_name
    class Meta:
        ordering = ['-created_at']