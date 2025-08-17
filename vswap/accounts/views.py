from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash

from accounts.models import UserProfile
from .forms import CustomUserChangeForm, CustomUserCreationForm, UserProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from posts.models import Post  # Adjust the import path if Post is in a different app


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


def profile_view(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(owner=request.user)
        return render(request, "accounts/profile.html", {"user": request.user, "posts": posts})
    else:
        return redirect("login")
    
@login_required
def user_update_view(request):
    user = request.user

    # พยายามดึง UserProfile ถ้าไม่มีให้สร้างขึ้นมาใหม่
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=user)

    if request.method == "POST":
        user_form = CustomUserChangeForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            update_session_auth_hash(request, user)  # ป้องกัน logout หลังเปลี่ยนข้อมูล
            return redirect("profile")
    else:
        user_form = CustomUserChangeForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "accounts/update_profile.html", context)

@login_required
def home_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, "accounts/home.html", {"posts": posts})
