import random
import string

from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Password, User
from .forms import PasswordForm, MyUserCreationForm, UserForm


# Create your views here.
def loginPage(request):

    page = "login"

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(
                request, "User does not exists !", extra_tags="usernotexists"
            )

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(
                request, "password does not match !", extra_tags="errorlogin"
            )

    context = {"page": page}
    return render(request, "base/login_register.html", context)


def registerUser(request):
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            print("SUCCESS")
            login(request, user)
            return redirect("home")
        else:
            messages.error(
                request, "An error occurred ! check password should be min 8 characters"
            )

    context = {"form": form}
    return render(request, "base/login_register.html", context)

def logoutUser(request):

    logout(request)
    return redirect("home")


@login_required(login_url="login")
def home(request):
    page = "home"
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    keys = Password.objects.filter(user=request.user)

    keys = keys.filter(Q(app_name__icontains=q) | Q(app_username__icontains=q))
    
    context = {"keys": keys, "query": q, "page": page}

    return render(request, "base/home.html", context)

#mobile password preview
@login_required(login_url="login")
def passwordPreview(request, pk):
    key = Password.objects.get(id=pk)
    return render(request, "base/password_preview.html", {"key": key})


@login_required(login_url="login")
def createPass(request):
    page = "create"
    form = PasswordForm()

    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    def Passwordgenerater():
        random.shuffle(characters)
        passwd = []
        for i in range(12):
            passwd.append(random.choice(characters))
        random.shuffle(passwd)
        genkey = "".join(passwd)
        return genkey

    if request.method == "POST":
        if request.POST.get("generate") != None:
            password = Passwordgenerater()
        else:
            password = request.POST.get("password")

        note = request.GET.get("note") if request.GET.get("note") != None else ""

        Password.objects.create(
            user=request.user,
            app_username=request.POST.get("app_username"),
            app_password=password,
            app_name=request.POST.get("app_name"),
            notes=note,
        )
        return redirect("home")  # home point to the url in the urls.py

    context = {"form": form, "page": page}

    return render(request, "base/password_form.html", context)


@login_required(login_url="login")
def updatePass(request, pk):

    key = Password.objects.get(id=pk)

    if request.user != key.user:
        return HttpResponse("You are not allowed here")

    if request.method == "POST":

        note = request.GET.get("note") if request.GET.get("note") != None else ""
        Password.objects.filter(id=pk).update(
            app_username=request.POST.get("app_username"),
            app_name=request.POST.get("app_name"),
            app_password=request.POST.get("key"),
            notes=note,
        )
        return redirect("home")

    return render(request, "base/password_form.html", {"key": key})


@login_required(login_url="login")
def deletePass(request, pk):

    key = Password.objects.get(id=pk)

    if request.user != key.user:
        return HttpResponse("You are not allowed here !")

    if request.method == "POST":
        key.delete()
        return redirect("home")

    return redirect("home")


@login_required(login_url="login")
def menu(request):
    return render(
        request,
        "base/menu.html",
    )


@login_required(login_url="login")
def UpdateUser(request, pk):
    
    user = User.objects.get(id=pk)
    if request.user != user:
        return HttpResponse("You are not allowed here")
    
    form = form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("menu")

    context = {"user": user, "form": form}
    return render(request, "base/update-user.html", context)


@login_required(login_url="login")
def deleteUser(request, pk):
    
    user = User.objects.get(id=pk)
    if request.user != user:
        return HttpResponse("You are not allowed here")

    if request.method == "POST":
        confirm = authenticate(request, email=user.email, password=request.POST.get('password'))
        if confirm:
            user.delete()
            return redirect("home")
        else:
            messages.error(
                request, "Password incorrect",extra_tags='incorrectpwd'
            )   

    context = {"user": user,}
    return render(request, "base/delete-user.html", context)


@login_required(login_url="login")
def settings(request):
    return render(
        request,
        "base/settings.html",
    )
