from django.urls import path
from . import views

urlpatterns = [
    path('api/get/', views.get_notifications_api, name='api_get_notifications'),

    path('api/read/<int:notification_id>/', views.mark_notification_as_read, name='api_mark_notification_read'),

]