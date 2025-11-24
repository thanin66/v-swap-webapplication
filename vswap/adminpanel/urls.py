from django.urls import path
from .views import admin_dashboard, delete_post, delete_user, admin_posts, admin_users

urlpatterns = [
    path('', admin_dashboard, name='admin_dashboard'),

    # Posts
    path('posts/', admin_posts, name='admin_posts'),
    path('posts/delete/<int:post_id>/', delete_post, name='delete_post'),

    # Users
    path('users/', admin_users, name='admin_users'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),


    path('posts/delete/<int:post_id>/', delete_post, name='delete_post'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),

]