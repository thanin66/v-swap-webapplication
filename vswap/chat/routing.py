from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # URL คือ ws://domain/ws/chat/<user_id>/
    re_path(r'ws/chat/(?P<id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]