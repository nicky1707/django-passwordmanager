from django.forms import ModelForm
from .models import Password,User
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']
    
class PasswordForm(ModelForm):
    
    class Meta:
        model = Password
        fields = '__all__'
        
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email']