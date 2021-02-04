from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Model and form import
from .models import Profile
from posts.models import Post, Comment, Like
from posts.forms import TweetForm
from .forms import RegisterForm, LoginForm, ProfileForm, ProfileRegisterForm
from .utils import get_followed_users, get_recommended_users

@login_required(login_url="user:login")
def profile_view(request, username):
    try:
        profile = Profile.objects.get(user=request.user)
        rec_users = get_recommended_users(profile)
        user = Profile.objects.get(user__username=username)
        posts = Post.objects.filter(owner=user)[:10]
    except profile.DoesNotExist or user.DoesNotExist:
        return HttpResponse("Not found.")
    else:
        if request.method == "POST":
            form = ProfileForm(files=request.FILES, data=request.POST, instance=user)
            if form.is_valid:
                form.save()
                return redirect("user:profile", username=username)
        else:
            form = ProfileForm(instance=user)

    context = {"profile":profile, "user":user, "posts":posts, "form":form, "unfollowed_users":rec_users}
    return render(request, "user/profile.html", context)

@login_required(login_url="user:login")
def home_view(request):
    user = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(owner_id__in=get_followed_users(user))[:10]
    rec_users = get_recommended_users(user)

    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = user
            instance.save()
            return redirect("user:home")
    else:
        form = TweetForm()

    context = {"form":form, "posts":posts, "user":user, "unfollowed_users":rec_users}
    return render(request, "user/home.html", context)

def login_register_view(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        register_form = RegisterForm(request.POST)
        profile_form = ProfileRegisterForm(request.POST)
        
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("user:home")

        if all([register_form.is_valid(), profile_form.is_valid()]):
            user = register_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.email = user.email
            profile.save()
            return redirect("user:login")
    else:
        login_form = LoginForm()
        register_form = RegisterForm()
        profile_form = ProfileRegisterForm(request.POST)

    context = {"login_form":login_form, "register_form":register_form, "profile_form":profile_form}
    return render(request, "register.html", context)

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("user:home")
            else:
                messages.warning(request, "Username or password incorrect. Try again.")
        else:
            messages.warning(request, "Username or password incorrect. Try again.")
    else:
        form = LoginForm()
    
    context = {"form":form}
    return render(request, "login.html", context)

def logout_view(request):
    logout(request)
    return redirect("user:login")