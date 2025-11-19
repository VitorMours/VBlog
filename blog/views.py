from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login 
from django.contrib.auth import logout as auth_logout
from blog.forms import LoginForm, SigninForm
from django.contrib.auth.decorators import login_required, permission_required

User = get_user_model()

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
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, email=email, password=password)
            print(user)
            if user is not None:
                auth_login(request, user)
                return redirect("dashboard")
            else:
                return render(request, 'login.html', { "form" : form }) 
        else:
            return render(request, 'login.html', { "form" : form })

    else:
        return HttpResponse("You can't use this HTTP method here", status=405)

def logout(request) -> None:
    logout(request)

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
                email = form.cleaned_data["email"]
            )
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
            auth_login(request, new_user)
            return redirect("dashboard")
        return render(request, "signin.html", { "form" : form })
    else:
        return HttpResponse("You can't use this HTTP method here", status=405)


@login_required(login_url="/login")
def dashboard(request):
    return render(request, "dashboard.html")