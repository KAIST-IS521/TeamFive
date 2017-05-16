from django.shortcuts import render
from .models import Post

def index(request):
    return render(request, 'bbs/index.html', {})

def list(request):
    posts = Post.objects.all()
    return render(request, 'bbs/list.html', {'posts': posts})

def write(request):
    if request.method == 'GET':
        return render(request, 'bbs/write.html', {})
    elif request.method == 'POST':
        return render(request, 'bbs/write.html', {})
