from django.shortcuts import redirect, render

from .auth import generate_challenge, get_service_pubkey, verify_response
from .models import BoardUser, Post


def index(request):
    return render(request, 'bbs/index.html', {})

def home(request):
    return render(request, 'bbs/home.html', {})

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
        return redirect("bbs/#List")

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
