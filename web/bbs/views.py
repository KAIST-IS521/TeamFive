from django.shortcuts import render, redirect
from .models import Post, BoardUser

def index(request):
    return render(request, 'bbs/index.html', {})

def list(request):
    posts = Post.objects.all()
    return render(request, 'bbs/list.html', {'posts': posts})

def write(request):
    if request.method == 'GET':
        return render(request, 'bbs/write.html', {})
    elif request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        use_script = (request.POST.get('use_script') == 'on')
        # TODO: Remove this and use current user from session.
        bogus_user = BoardUser.objects.all()[0]
        post = Post(title=title, content=content, allow_script=use_script, author=bogus_user)
        post.save()
        return redirect('list')
