from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),


    path("home/", views.home_view, name="home"),
    
    path("profile/", views.profile_view, name="profile"),
    path("update_profile/", views.user_update_view, name="update_profile"),
    path('profile/<int:user_id>/', views.profile_view, name='profile_by_id'),

]