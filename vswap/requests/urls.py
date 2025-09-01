from django.urls import path
from . import views

urlpatterns = [
    path('', views.request_list, name='requests'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('<int:post_id>/send/', views.send_request, name='send_request'),
    path('<int:request_id>/<str:action>/', views.respond_request, name='respond_request'),
]