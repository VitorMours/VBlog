from django.shortcuts import render, redirect
from django.http import HttpResponse
from blog.forms import LoginForm, SigninForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

def index(request):
    if request.method == "GET":
        return render(request, 'index.html')
    else:
        return HttpResponse("You can't use this HTTP method here", status=405)
    
def about(request):
    if request.method == "GET":
        return render(request, 'about.html')

@never_cache    
@csrf_protect
def login(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect("/protected")
    
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {"form":form})
    
    if request.method == "POST":
        form = LoginForm(request.POST)

        if not form.is_valid():
            messages.error(request, "Please correct the errors below.")
            return render(request, 'login.html', {"form": form})
        
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        
        user = authenticate(
            request, 
            email=email, 
            password=password
        )

        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            
            next_url = request.GET.get('next', '/protected')
            return redirect(next_url)
            
        else:
            messages.error(
                request, 
                "Invalid username or password. Please try again."
            )
            return render(request, 'login.html', {"form": form})
    
    else:
        return HttpResponse("Method not allowed", status=405)

@require_http_methods(["GET", "POST"])
@csrf_protect
@never_cache
def logout(request):
    if request.user.is_authenticated:
        username = request.user.username
        auth_logout(request)
        messages.success(request, f"Goodbye {username}! You have been successfully logged out.")
    return redirect("index")

@csrf_protect
def signin(request):
    if request.method == "GET":
        form = SigninForm()
        return render(request, 'signin.html', {"form": form})

    elif request.method == "POST":
        form = SigninForm(request.POST)

        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data["email"]).exists():
                messages.error(request, "email already exists")
                return render(request, 'signin.html', {"form": form})
            
            if User.objects.filter(email=form.cleaned_data["username"]).exists():
                messages.error(request, "Username already registered")
                return render(request, 'signin.html', {"form": form})

            new_user = User.objects.create_user(
                username=form.cleaned_data["username"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
            )
            new_user.set_password(form.cleaned_data["password"])
            
            user = authenticate(request, 
                                username=form.cleaned_data["username"], 
                                password=form.cleaned_data["password"])
            new_user.save()
            
            auth_login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("/protected")
        
        else: 
            messages.warning(request, "One of this credentials is already in use")
            return redirect("/signin")
                
    else:
        return HttpResponse("You can't use this HTTP method here", status=405)
    
@login_required
def protected_route(request):
    return HttpResponse("Hi", status=200)