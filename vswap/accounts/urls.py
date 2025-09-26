from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),


    path("home/", views.home_view, name="home"),
    
    path("profile/", views.profile_view, name="profile"),
    path("update_profile/", views.user_update_view, name="update_profile"),
    path("profile/<int:user_id>/", views.profile_view, name="profile_detail"),

    path("map/", views.map_view, name="map"), 

]