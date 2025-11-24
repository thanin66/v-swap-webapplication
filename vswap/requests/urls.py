from django.urls import path
from . import views

urlpatterns = [
    path('', views.request_page, name='requests'),
    path('<int:post_id>/send/', views.send_request, name='send_request'),


    path('<int:request_id>/<str:action>/', views.respond_request, name='respond_request'),
    path('request-page/', views.request_page, name='request_page'),

    path('cancel/<int:request_id>/', views.cancel_request, name='cancel_request'),

    path('confirm/<int:request_id>/', views.request_confirm, name='request_confirm'),

    path('api/accept/status/<int:request_id>/', views.get_accept_status),
    path('api/accept/submit/<int:request_id>/', views.submit_accept),
    path('api/accept/cancel/<int:request_id>/', views.cancel_accept),


    path('map/confirm/<int:request_id>/', views.request_map_confirm, name='request_map_confirm'),
    path('api/map/status/<int:request_id>/', views.api_map_status, name='api_get_map_status'),
    path('api/map/submit/<int:request_id>/', views.api_submit_map_position, name='api_submit_map_position'),

    path("next-step/<int:request_id>/", views.next_step, name="next_step"),
    path('posts/update-multiple-status/', views.update_multiple_post_status, name='update_multiple_post_status'),

]