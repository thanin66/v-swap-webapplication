from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from posts.models import Post
from django.contrib.auth import get_user_model


User = get_user_model()

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    return render(request, 'adminpanel/admin_dashboard.html')


@user_passes_test(lambda u: u.is_staff)
def admin_posts(request):
    posts = Post.objects.all()
    return render(request, 'adminpanel/admin_posts.html', {'posts': posts})

@user_passes_test(lambda u: u.is_superuser)
def admin_users(request):
    users = User.objects.all()
    return render(request, "adminpanel/admin_users.html", {"users": users})

@user_passes_test(lambda u: u.is_staff)
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('admin_posts')


@user_passes_test(lambda u: u.is_staff)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not user.is_superuser:
        user.delete()
    return redirect('admin_users')


@user_passes_test(lambda u: u.is_superuser)
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('admin_posts')


@user_passes_test(lambda u: u.is_staff)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_superuser:
        return redirect('admin_users')

    user.delete()
    return redirect('admin_users')