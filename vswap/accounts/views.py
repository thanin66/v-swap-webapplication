# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from accounts.models import CustomUser, UserProfile
from .forms import CustomUserChangeForm, CustomUserCreationForm, UserProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from posts.models import Post  # Adjust the import path if Post is in a different app

#register view
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            next_url = request.GET.get("next", "home")
            return redirect(next_url)
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})



#login view
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get("next", "home")
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})

#logout view
def logout_view(request):
    logout(request)
    return redirect("login")

#get profile by id
def get_profile_by_id(user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        profile, created = UserProfile.objects.get_or_create(user=user)
        return profile
    except CustomUser.DoesNotExist:
        return None
    
@login_required
def profile_view(request, user_id=None):
    if user_id:
        user = get_object_or_404(CustomUser, id=user_id)
    else:
        user = request.user

    posts = Post.objects.filter(owner=user)
    tabs = ["all", "swap", "buy_sell", "donation"]

    return render(request, "accounts/profile.html", {
        "user": user,       # key ที่ template ใช้
        "posts": posts,
        "tabs": tabs,
    })


#update profile view
@login_required
def user_update_view(request):
    user = request.user
    profile = user.userprofile

    if request.method == "POST":
        user_form = CustomUserChangeForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your profile was updated successfully!")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        user_form = CustomUserChangeForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "accounts/update_profile.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })

#home view
@login_required
def home_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, "accounts/home.html", {"posts": posts})

