from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    posts = Post.objects.all().order_by('-timestamp')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page') or 1
    page_obj = paginator.page(page_number)

    return render(request, "network/index.html",{
        'page_obj': page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def new_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        post = Post.objects.create(user=request.user, content=content)
    return HttpResponseRedirect(reverse("index"))

def profile(request, username):
    user = User.objects.get(username=username)
    posts = user.posts.all().order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page') or 1
    page_obj = paginator.page(page_number)
    follower_count = user.followers.count()
    following_count = user.following.count()

    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(user=request.user, following_user=user).exists()

    return render(request, 'network/profile.html', {
        'user': user,
        'page_obj': page_obj,
        'follower_count': follower_count,
        'following_count': following_count,
        'is_following': is_following
    })

@login_required
def follow(request, username):
    if request.method == 'POST':
        following_user = User.objects.get(username=username)
        follow = Follow.objects.create(user=request.user, following_user=following_user)
    return HttpResponseRedirect(reverse("profile", args=[username]))

@login_required
def unfollow(request, username):
    if request.method == 'POST':
        following_user = User.objects.get(username=username)
        follow = Follow.objects.get(user=request.user, following_user=following_user)
        follow.delete()
    return HttpResponseRedirect(reverse("profile", args=[username]))

@login_required
def following(request):
    following_user_ids = request.user.following.values_list('following_user_id', flat=True)
    posts = Post.objects.filter(user_id__in=following_user_ids).order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page') or 1
    page_obj = paginator.page(page_number)
    return render(request, 'network/following.html', {'page_obj': page_obj})

@csrf_exempt
@login_required
def edit_post(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        if post.user == request.user:
            data = json.loads(request.body)
            content = data.get('content', '')
            post.content = content
            post.save()
            return JsonResponse({'success': True, 'message': 'Post updated successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Unauthorized'})
    else:
        HttpResponseRedirect(reverse("index"))

@csrf_exempt
@login_required
def like_post(request, post_id, action):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        print(action)
        if action == 'like':
            post.likes.add(request.user)
        elif action == 'unlike':
            post.likes.remove(request.user)
        else:
            return JsonResponse({'success': False}, status=400)
        
        return JsonResponse({'success': True, 'like_count': post.likes.count()})
    
    return JsonResponse({'success': False}, status=405)