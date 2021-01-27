from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Model and form import
from .models import Profile
from posts.models import Post, Comment, Like
from posts.forms import TweetForm
from .forms import RegisterForm, LoginForm, ProfileForm
from .utils import get_followed_users


# CBS for home page, lists Posts of followed users
# class ProfileView(LoginRequiredMixin, ListView):
#     template_name = "user/profile.html"
#     model = Post
#     form_class = ProfileForm
#     login_url = '/register/'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         username = self.kwargs.get("username")
#         profile = Profile.objects.get(user=self.request.user)
#         user = Profile.objects.get(user__username=username)
#         posts = Post.objects.filter(owner=user)
#         context["posts"] = posts
#         context["user"] = user
#         context["profile"] = profile
#         return context

#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         return render(request, self.template_name, {'form': form})

#     def post(self, request, *args, **kwargs):
#         form = form = self.form_class(self.request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect(self.template_name)

@login_required(login_url="user:login")
def profile_view(request, username):
    try:
        profile = Profile.objects.get(user=request.user)
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

    context = {"profile":profile, "user":user, "posts":posts, "form":form}
    return render(request, "user/profile.html", context)

@login_required(login_url="user:login")
def home_view(request):
    user = Profile.objects.get(user=request.user)
    # followed_users = [*user.following.all().values_list("follower_id", flat=True).distinct()]
    # followed_users.append(user.id)
    posts = Post.objects.filter(owner_id__in=get_followed_users(user)).order_by("-created_on")[:10]

    if request.method == "POST":
        form = TweetForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = user
            instance.save()
            return redirect("user:home")
            form = TweetForm()
    else:
        form = TweetForm()

    context = {"form":form, "posts":posts, "user":user}
    return render(request, "user/home.html", context)

# def login_register_view(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data["username"]
#             password = form.cleaned_data["password"]
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, "You have been succesfully logged in.")
#                 return redirect("user:home")
#             else:
#                 messages.warning(request, "Username or password incorrect. Try again.")
#         else:
#             messages.warning(request, "Username or password incorrect. Try again.")
#     else:
#         form = LoginForm()
#     context = {"form":form}
#     return render(request, "register.html", context)

def login_register_view(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        register_form = RegisterForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("user:home")

        if register_form.is_valid():
            register_form.save()
            return redirect("user:login")
    else:
        login_form = LoginForm()
        register_form = RegisterForm()

    context = {"login_form":login_form, "register_form":register_form}
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