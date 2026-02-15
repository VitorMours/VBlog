from datetime import timezone
import uuid
import json
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
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
from blog.services.voting_service import VotingService
from blog.services.ai.service import GeminiService
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
    post_views = VisualizationService.calculate_views_per_post(user)
    views_today = VisualizationService.count_views_today(user)
    views_per_day = VisualizationService.calculate_views_per_day(user, days=7)
    
    titles = [item["post___title"] for item in post_views]
    views = [item["total_views"] for item in post_views]
    
    context = {
        "user_name": user.get_full_name() or user.first_name or user.username,
        "user_views": user_views,
        "avg_views": avg_views,
        "titles":titles,
        "views":views,
        "views_today": views_today,
        "user": user,  # Passar o objeto user completo para o template
    }
    
    return render(request, "profile.html", context)

@login_required(login_url="/login")
def ai_action(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método inválido"}, status=405)

    action = request.POST.get("action")
    content = request.POST.get("content")

    if not content:
        return JsonResponse({"error": "Texto vazio"}, status=400)

    if action == "improve":
        result = GeminiService.improve_post(content)
        print(result)
        
    elif action == "title":
        result = GeminiService.summarize_post(content)
        print(result)

    else:
        return JsonResponse({"error": "Ação inválida"}, status=400)

    return JsonResponse({"result": result})

@login_required(login_url="/login")
def vote_on_post(request, post_id: uuid):
    """
    API endpoint para registrar/atualizar/remover votos em posts.
    Espera uma requisição POST com JSON contendo 'vote_value' (true para upvote, false para downvote)
    """
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Método HTTP não permitido"}, status=405)
    
    try:
        post = get_object_or_404(Post, pk=post_id)
        data = json.loads(request.body)
        vote_value = data.get("vote_value")
        
        if not isinstance(vote_value, bool):
            return JsonResponse({"success": False, "message": "vote_value deve ser um booleano"}, status=400)
        
        success, message = VotingService.add_or_update_vote(post, request.user, vote_value)
        
        if success:
            # Calcular dados atualizados após o voto
            current_status = post._status
            user_vote = VotingService.get_user_vote(post, request.user)
            
            return JsonResponse({
                "success": True,
                "message": message,
                "status": current_status,
                "user_vote": user_vote.vote_value if user_vote else None
            })
        else:
            return JsonResponse({"success": False, "message": message}, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "message": f"Erro ao processar voto: {str(e)}"}, status=500)