from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from blog.forms import LoginForm, SigninForm
from django.contrib.auth.models import User

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
        return render(request, 'login.html', { "form" : form })

    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            return HttpResponse("Good!", status=200)
            # precisa adicionar a autenticacao e todos os outros processos
        else:
            return render(request, 'login.html', { "form" : form })


    else:
        return HttpResponse("You can't use this HTTP method here", status=405)

def signin(request):
    if request.method == "GET":
        form = SigninForm()
        return render(request, 'signin.html', { "form" : form })
    elif request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            new_user = User(
                first_name = form.cleaned_data["first_name"],
                last_name = form.cleaned_data["last_name"],
                username = form.cleaned_data["username"],
                email = form.cleaned_data["email"],
            )
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
            return redirect("dashboard")
        return render(request, "signin.html", { "form" : form })
    else:
        return HttpResponse("You can't use this HTTP method here", status=405)

def dashboard(request):
    return render(request, "dashboard.html")