from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),

    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),

    path('post/create/<str:post_type>/', views.post_create, name='post_create'),

    path("map/", views.map_view, name="map"), 

    path('search/', views.search_view, name='search'), # ต้องมี slash (/) ปิดท้าย
    
    path('search/results/', views.search_page, name='search_page'),

    path('report/<int:pk>/', views.report_post, name='report_post')
]
