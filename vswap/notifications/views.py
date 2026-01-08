from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
import json


@login_required
def get_notifications_api(request):
    # ดึงแจ้งเตือนของ User นี้ ที่ยังไม่ได้อ่าน (เรียงใหม่สุดก่อน)
    notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at')
    
    data = {
        'count': notifications.count(),
        'notifications': [
            {
                'id': n.id,
                'message': n.message,
                'link': n.link if n.link else '#',
                'type': n.type,
                'created_at': n.created_at.strftime('%d/%m/%Y %H:%M') # จัดรูปแบบวันที่ตามต้องการ
            } for n in notifications
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