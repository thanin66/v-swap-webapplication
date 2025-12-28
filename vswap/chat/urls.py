from django.urls import path
from . import views

urlpatterns = [

    path('', views.chat_home, name='chat_home'),
    
    path('<int:user_id>/', views.chat_room, name='chat_room'),

    path('sidebar-api/<int:active_user_id>/', views.chat_sidebar_partial, name='chat_sidebar_api'),

]