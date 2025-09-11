from django.shortcuts import render
from django.http import HttpResponse
from blog.forms import LoginForm 

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
def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html')
    else:
        return HttpResponse("You can't use this HTTP method here", status=405)