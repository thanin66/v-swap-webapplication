from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Message

User = get_user_model()

@login_required
def chat_room(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    # 1. MARK AS READ: อ่านข้อความที่ 'other_user' ส่งมาหาเรา
    # เฉพาะข้อความที่ยังไม่อ่าน (is_read=False) ให้แก้เป็น True
    Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)

    # 2. ดึงประวัติการคุย (เหมือนเดิม)
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | 
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')

    # 3. Sidebar Logic (เพิ่มส่วนนับ unread)
    sent_to = Message.objects.filter(sender=request.user).values_list('receiver', flat=True)
    received_from = Message.objects.filter(receiver=request.user).values_list('sender', flat=True)
    contact_ids = set(sent_to) | set(received_from)
    
    chat_list = []
    for contact_id in contact_ids:
        friend = User.objects.get(id=contact_id)
        
        last_msg = Message.objects.filter(
            Q(sender=request.user, receiver=friend) | 
            Q(sender=friend, receiver=request.user)
        ).order_by('-timestamp').first()
        
        # +++ เพิ่มตรงนี้: นับจำนวนที่เพื่อนส่งมาแล้วเรายังไม่อ่าน +++
        unread_count = Message.objects.filter(sender=friend, receiver=request.user, is_read=False).count()
        
        chat_list.append({
            'friend': friend,
            'last_message': last_msg.content if last_msg else "",
            'timestamp': last_msg.timestamp if last_msg else None,
            'is_active': (friend.id == other_user.id),
            'unread_count': unread_count # ส่งค่าไปหน้าเว็บ
        })
    
    chat_list.sort(key=lambda x: x['timestamp'] if x['timestamp'] else "", reverse=True)

    return render(request, 'chat/room.html', { 
        'other_user': other_user,
        'messages': messages,
        'chat_list': chat_list, 
    })

@login_required
def chat_sidebar_partial(request, active_user_id=None):
    # Logic การดึงรายชื่อ (เหมือนใน chat_room แต่แยกออกมา)
    sent_to = Message.objects.filter(sender=request.user).values_list('receiver', flat=True)
    received_from = Message.objects.filter(receiver=request.user).values_list('sender', flat=True)
    contact_ids = set(sent_to) | set(received_from)
    
    chat_list = []
    for contact_id in contact_ids:
        friend = User.objects.get(id=contact_id)
        
        # หาข้อความล่าสุด
        last_msg = Message.objects.filter(
            Q(sender=request.user, receiver=friend) | 
            Q(sender=friend, receiver=request.user)
        ).order_by('-timestamp').first()
        
        # นับจำนวนที่ยังไม่อ่าน
        unread_count = Message.objects.filter(sender=friend, receiver=request.user, is_read=False).count()
        
        chat_list.append({
            'friend': friend,
            'last_message': last_msg.content if last_msg else "",
            'timestamp': last_msg.timestamp if last_msg else None,
            # ตรวจสอบว่าใครคือคนที่ Active อยู่ เพื่อใส่สีฟ้าที่แถบชื่อ
            'is_active': (friend.id == int(active_user_id)) if active_user_id else False,
            'unread_count': unread_count
        })
    
    chat_list.sort(key=lambda x: x['timestamp'] if x['timestamp'] else "", reverse=True)

    # Return กลับไปแค่ชิ้นส่วน HTML (Partial)
    return render(request, 'chat/chat_list.html', {'chat_list': chat_list})


@login_required
def chat_home(request):
    # 1. ค้นหาข้อความล่าสุด
    last_msg = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-timestamp').first()

    if last_msg:
        # 2. ถ้าเจอประวัติ -> ไปห้องแชทล่าสุด
        if last_msg.sender == request.user:
            target_user = last_msg.receiver
        else:
            target_user = last_msg.sender
            
        return redirect('chat_room', user_id=target_user.id)
    
    return render(request, 'chat/no_chat.html')