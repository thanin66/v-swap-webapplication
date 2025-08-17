from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:pk>/', views.post_detail, name='post_detail'),

    # ใช้สำหรับ form ทั่วไป (ไม่ใช้แล้วถ้าต้องเลือกประเภทก่อน)
    # path('create/', views.post_create, name='post_create_no_type'),

    path('<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('<int:pk>/update/', views.post_edit, name='post_update'),

    path('post/type/', views.post_type_select, name='post_type_select'),  # หน้าเลือกประเภท
    path('post/create/<str:post_type>/', views.post_create, name='post_create'),  # สร้างโพสต์แบบมีประเภท
    path('posts/post/create/<str:post_type>/', views.post_create, name='post_create'),

]