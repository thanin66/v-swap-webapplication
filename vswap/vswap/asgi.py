import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing  # ตรวจสอบว่ามีไฟล์ chat/routing.py อยู่จริง

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vswap.settings')

application = ProtocolTypeRouter({
    # HTTP ให้ Django จัดการเหมือนเดิม
    "http": get_asgi_application(),
    
    # WebSocket ให้ Channels จัดการ
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})