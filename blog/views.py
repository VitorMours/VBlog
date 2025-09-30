from django.shortcuts import render, redirect
from django.http import HttpResponse
from blog.forms import LoginForm, SigninForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate


def index(request):
    if request.method == "GET":
        return render(request, 'index.html')
    else:
        return HttpResponse("You can't use this HTTP method here", status=405)
    
def about(request):
    if request.method == "GET":
        return render(request, 'about.html')
    
def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {"form":form})
    else:
        return HttpResponse("You can't use this HTTP method here", status=405)

def logout(request):
    auth_logout(request)
    return redirect("/")

def signin(request):
    if request.method == "GET":
        form = SigninForm()
        return render(request, 'signin.html', {"form": form})

    elif request.method == "POST":
        form = SigninForm(request.POST)

        for field in form.data.items():
            if field[1] == None or field[1] == "":
                messages.error(request, "All data need to be filled")
                return redirect("signin")
            
        search_by_email = User.objects.filter(email=form.data["email"])
        search_by_username = User.objects.filter(username=form.data["username"])

        if not search_by_email.exists() and not search_by_username.exists():
            new_user = User.objects.create_user(
                username=form.data["username"],
                first_name=form.data["first_name"],
                last_name=form.data["last_name"],
                email=form.data["email"],
                password=form.data["password"],
            )
            new_user.save()
            user = authenticate(request, 
                                username=form.data["username"], 
                                password=form.data["password"])
            auth_login(request, new_user)
            return redirect("/protected")

        else: 
            messages.warning(request, "One of this credentials is already in use")
            return redirect("/signin")
                
    else:
        return HttpResponse("You can't use this HTTP method here", status=405)
    
@login_required
def protected_route(request):
    return HttpResponse("Hi", status=200)