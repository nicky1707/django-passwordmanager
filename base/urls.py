from django.urls import path
from . import views

urlpatterns = [
    path("account/login/",views.loginPage, name="login"),
    path("account/logout/",views.logoutUser, name="logout"),
    path("account/register/",views.registerUser, name="register"),
    path('account/update/<str:pk>/',views.UpdateUser,name='update-user'),
    path('account/delete/<str:pk>/',views.deleteUser,name='delete-user'),
    
    
    path('',views.home,name='home'),
    path('account/',views.menu,name='menu'),
    path('account/settings/',views.settings,name='settings'),
    
    path('password/create/',views.createPass,name='create-pass'),
    path("password/<str:pk>/",views.passwordPreview, name="password"),
    path('password/update/<str:pk>/',views.updatePass,name='update-pass'),
    path('password/delete/<str:pk>/',views.deletePass,name='delete-pass'),
]
