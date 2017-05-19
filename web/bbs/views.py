from django.shortcuts import redirect, render

from .auth import generate_challenge, get_service_pubkey, verify_response
from .models import Post

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method == 'GET':
        return render(request, 'bbs/login.html', {})
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("list")
        else:
            return redirect("auth_index")

@login_required(login_url='/bbs/login')
def logout(request):
    auth.logout(request)
    return redirect("index")

def index(request):
    return render(request, 'bbs/index.html', {})

@login_required(login_url='/bbs/login')
def list(request):
    posts = Post.objects.all()
    return render(request, 'bbs/list.html', {'posts': posts})

def check_post_permission(user, post, use_script):
    if use_script and not user.has_perm('use_script'):
        return False
    if post and post.author != user:
        return False
    return True

@login_required(login_url='/bbs/login')
def write(request):
    if request.method == 'GET':
        return render(request, 'bbs/write.html', {})
    elif request.method == 'POST':
        user = request.user
        title = request.POST.get('title')
        content = request.POST.get('content')
        use_script = 'use_script' in request.POST
        if check_post_permission(user, None, use_script):
            post = Post(title=title, content=content, use_script=use_script, author=user)
            post.save()
        return redirect("list")

@login_required(login_url='/bbs/login')
def read(request, post_id):
    try:
        post = Post.objects.get(id=int(post_id))
    except ObjectDoesNotExist:
        return redirect('list')
    return render(request,
                  'bbs/read.html',
                  {
                      'id': post.id,
                      'title': post.title,
                      'content': post.content,
                      'author': post.author.username
                  })

@login_required(login_url='/bbs/login')
def delete(request, post_id):
    try:
        post = Post.objects.get(id=int(post_id))
    except ObjectDoesNotExist:
        return redirect('list')
    if post.author == request.user:
        post.delete()
    return redirect('list')

@login_required(login_url='/bbs/login')
def edit(request, post_id):
    try:
        post = Post.objects.get(id=int(post_id))
    except ObjectDoesNotExist:
        return redirect('list')
    if request.method == 'GET':
        return render(request,
                      'bbs/edit.html',
                      {
                          'id': post.id,
                          'title': post.title,
                          'content': post.content
                      })
    elif request.method == 'POST':
        user = request.user
        title = request.POST.get('title')
        content = request.POST.get('content')
        use_script = 'use_script' in request.POST
        if check_post_permission(user, post, use_script):
            post.title = title
            post.content = content
            post.use_script = use_script
            post.save()
        return redirect("list")

def auth_index(request):
    return render(request, 'bbs/auth_index.html', {})

def auth_chal(request):
    if request.method == 'POST':
        auth_id = request.POST.get('id')
        challenge = generate_challenge(auth_id)
        if challenge is not None:
            nonce, enc_nonce = challenge
            request.session['auth_id'] = auth_id
            request.session['auth_nonce'] = nonce
            service_pubkey = get_service_pubkey()
            context = {
                'auth_id': auth_id,
                'enc_nonce': enc_nonce,
                'service_pubkey': service_pubkey
            }
            return render(request, 'bbs/auth_chal.html', context)
    return redirect('auth_index')

def auth_resp(request):
    if request.method == 'POST':
        auth_resp = request.POST.get('auth_resp')
        auth_nonce = request.session['auth_nonce']
        auth_id = request.session['auth_id']
        if verify_response(auth_nonce, auth_resp):
            print("Auth success for {}".format(auth_id))
        else:
            print("Auth failed")
        return redirect('index')
    return redirect('auth_index')
