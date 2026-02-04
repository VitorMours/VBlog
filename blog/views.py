from datetime import timezone
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
    user_views = VisualizationService.count_user_views(user)
    avg_views = VisualizationService.calculate_views_per_post_avg(user)
    views_today = VisualizationService.count_views_today(user)
    views_per_day = VisualizationService.calculate_views_per_day(user, days=7)
    
    chart_labels_daily = []
    chart_data_daily = []
    
    for item in views_per_day:
        date_str = item['date']
        if isinstance(date_str, str):
            if 'T' in date_str:
                date_obj = timezone.datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                formatted_date = date_obj.strftime('%d/%m')
            else:
                formatted_date = date_str
        else:
            formatted_date = date_str.strftime('%d/%m')
        
        chart_labels_daily.append(formatted_date)
        chart_data_daily.append(item['total_views'])
    
    if not chart_labels_daily:
        chart_labels_daily = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab', 'Dom']
        chart_data_daily = [0, 0, 0, 0, 0, 0, 0]
    
    views_per_post_data = VisualizationService.calculate_views_per_post(user)
    
    chart_labels_posts = []
    chart_data_posts = []
    
    for item in views_per_post_data[:10]:
        post_title = item.get("", 'Post Sem Título')
        if post_title and len(post_title) > 20:
            display_title = post_title[:20] + '...'
        else:
            display_title = post_title or 'Post'
        
        chart_labels_posts.append(display_title)
        chart_data_posts.append(item['total_views'])
    
    if not chart_labels_posts:
        chart_labels_posts = ['Sem dados disponíveis']
        chart_data_posts = [0]
    
    context = {
        "user_name": user.get_full_name() or user.first_name or user.username,
        "user_views": user_views,
        "avg_views": avg_views,
        "views_today": views_today,
        "chart_labels_daily": chart_labels_daily,
        "chart_data_daily": chart_data_daily,
        "chart_labels_posts": chart_labels_posts,
        "chart_data_posts": chart_data_posts,
        "user": user,  # Passar o objeto user completo para o template
    }
    
    return render(request, "profile.html", context)