from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from httpx import request
from .models import Notification
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
import json


@login_required
def get_notifications_api(request):

    unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()   
    all_notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')[:20]

    data = {
            'count': unread_count, # ส่งจำนวนที่ยังไม่อ่านไป
            'notifications': [
                {
                    'id': n.id,
                    'message': n.message,
                    'link': n.link if n.link else '#',
                    'type': n.type,
                    'is_read': n.is_read, 
                    'created_at': n.created_at.strftime('%d/%m %H:%M')
                } for n in all_notifications
            ]
        }
    
    return JsonResponse(data)

@login_required
@require_POST # บังคับว่าต้องส่งเป็น POST มาเท่านั้นเพื่อความปลอดภัย
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})