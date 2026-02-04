import uuid
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login 
from django.contrib.auth import logout as auth_logout
from blog.forms import LoginForm, PostForm, SigninForm
from django.contrib.auth.decorators import login_required, permission_required
from blog.models import Post, CustomUser, Visualization
from django.contrib import messages
from blog.services.visualization_service import VisualizationService
from blog.services.message_service import MessageService
from blog.services.message_service import MessageImportanceLevel
from blog.services.auth_service import AuthService
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
    if request.user.is_authenticated:
            return redirect("relevants")

    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', { "form" : form })

    elif request.method == "POST":
        form = LoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
         
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("relevants")
            else:
                messages.error(request, "Email ou senha incorretos. Por favor, tente novamente.")
                return render(request, 'login.html', { "form" : form }) 
        else:
            return render(request, 'login.html', { "form" : form })

    else:
        return HttpResponse("You can't use this HTTP method here", status=405)

def logout(request) -> None:
    auth_logout(request)
    return redirect("index")

def signin(request):
    if request.method == "GET":
        form = SigninForm()
        return render(request, 'signin.html', { "form" : form })
    
    elif request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            
            if result := AuthService.check_if_email_is_registered(email):
                messages.info(request, "Ja existe um usuario com esse login")
                return redirect("signin")

            new_user = User(
                first_name = form.cleaned_data["first_name"],
                last_name = form.cleaned_data["last_name"],
                email = form.cleaned_data["email"]
            )
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
            auth_login(request, new_user)
            return redirect("relevants")
        return render(request, "signin.html", { "form" : form })
    else:
        return HttpResponse("You can't use this HTTP method here", status=405)

@login_required(login_url="/login")
def recents(request):
    if request.method != "GET":
        return HttpResponse("You can't use this HTTP method here", status=405)

    posts = Post.objects.all().order_by("-_created_at")
    context = { "posts": posts }

    return render(request, "recents.html", context=context)

@login_required(login_url="/login")
def relevants(request): 

    if request.method != "GET":
        return HttpResponse("You can't use this HTTP method here", status=405)

    posts = Post.objects.all().order_by("-_status")
    context = { "posts": posts }

    return render(request, "relevants.html", context=context)

@login_required(login_url="/login")
def create_post(request):
    if request.method == "GET":
        form = PostForm()
        return render(request, "create_post.html", { "form" : form })

    elif request.method == "POST":
        form = PostForm(request.POST) 
        if form.is_valid():
            new_post = Post(
                title=form.cleaned_data["title"],
                content=form.cleaned_data["content"],
                owner = request.user
            )            
            new_post.save()
            
            return redirect("relevants")
        return render(request, "create_post.html", { "form": form })        
    
    return render(request, "create_post.html")

@login_required(login_url="/login")
def view_post(request, id: uuid):
    post = get_object_or_404(Post, pk=id)
    
    new_view = Visualization(
        user = request.user,
        post = post
    )
    
    new_view.save()
    
    return render(request, "post.html", { "post" : post })



@login_required(login_url="/login")
def profile(request):
    user = request.user 
    user = CustomUser.objects.filter(email=user).first()
    user_views = VisualizationService.get_user_views(user)

    context = {"user_name": user.first_name, "user_views": user_views }
    return render(request, "profile.html", context)