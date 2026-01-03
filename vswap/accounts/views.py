# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from accounts.models import CustomUser, UserProfile
from .forms import CustomUserChangeForm, CustomUserCreationForm, UserProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from posts.models import Post, Swap, BuySell, Donation
from django.utils.http import url_has_allowed_host_and_scheme
from itertools import chain
from django.core.paginator import Paginator
from operator import attrgetter



#home view
@login_required
def home_view(request):
    swaps = Swap.objects.all().order_by('-created_at')[:4]      # เอามา 4 อัน
    sales = BuySell.objects.all().order_by('-created_at')[:4]    # เอามา 4 อัน
    donations = Donation.objects.all().order_by('-created_at')[:4] # เอามา 4 อัน
    if len(swaps) >=4 and len(sales) >=4 and len(donations) >=4:
        all_posts = list(chain(swaps, sales, donations))
    else:
        all_posts = list(chain(swaps, sales, donations))
    all_posts.sort(key=lambda x: x.created_at, reverse=True)

    latest_posts = all_posts[:8]

    return render(request, 'accounts/home.html', {
        'posts': latest_posts
    })

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
            next_url = request.GET.get("next")
            if next_url and url_has_allowed_host_and_scheme(url=next_url, allowed_hosts=request.get_host()):
                return redirect(next_url)
            return redirect("home")
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
    
    # 1. ดึงข้อมูลจากตารางลูก (Child Tables) เพื่อให้ได้ field ครบๆ (price, condition)
    swaps = Swap.objects.filter(owner=user)
    # buy_sell รวมทั้ง Sale และ Wishlist ไว้ด้วยกัน
    buysells = BuySell.objects.filter(owner=user) 
    # donation ต้องดูว่าใน DB เก็บ post_type เป็น 'donate' หรือ 'donation' (ตาม Model คือ 'donate')
    donations = Donation.objects.filter(owner=user)

    # 2. รวมและเรียงลำดับตามวันที่ (ล่าสุดขึ้นก่อน)
    posts = sorted(
        chain(swaps, buysells, donations),
        key=attrgetter('created_at'),
        reverse=True
    )

    # Tabs สำหรับหน้าเว็บ
    tabs = ["all", "swap", "sale", "wishlist", "donation"]

    return render(request, "accounts/profile.html", {
        "user": user,
        "posts": posts,
        "tabs": tabs,
    })


#update profile view
@login_required
def user_update_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

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

