# requests/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from posts.models import Post
from .models import Request
from .forms import SwapRequestForm, SaleRequestForm, DonateRequestForm

@login_required
def send_request(request, post_id):
    target_post = get_object_or_404(Post, id=post_id)
    post_type = target_post.post_type

    # ตรวจสอบว่าผู้ใช้กำลังส่งคำขอหาโพสต์ของตัวเองหรือไม่
    if request.user == target_post.owner:
        messages.error(request, "คุณไม่สามารถส่งคำขอสำหรับโพสต์ของคุณเองได้")
        return redirect('post_detail', pk=target_post.id)
    
    # ตรวจสอบว่ามีคำขอที่รอดำเนินการอยู่แล้วหรือไม่
    if Request.objects.filter(requester=request.user, post=target_post, status='pending').exists():
        messages.warning(request, "คุณได้ส่งคำขอสำหรับโพสต์นี้ไปแล้วและกำลังรอการตอบกลับ")
        return redirect('post_detail', pk=target_post.id)

    # จัดการการประมวลผลคำขอ (POST request)
    if request.method == 'POST':
        if post_type == 'swap':
            form = SwapRequestForm(request.POST, user=request.user)
        elif post_type == 'buy_sell':
            form = SaleRequestForm(request.POST)
        elif post_type == 'donate':
            form = DonateRequestForm(request.POST)
        else:
            messages.error(request, "ไม่สามารถสร้างคำขอสำหรับโพสต์ประเภทนี้ได้")
            return redirect('post_detail', pk=target_post.id)

        if form.is_valid():
            new_request = Request.objects.create(
                post=target_post,
                request_type=post_type,
                requester=request.user,
                message=form.cleaned_data.get('message', ''),
                amount=form.cleaned_data.get('amount', None),
                offered_product=form.cleaned_data.get('offered_product', None),
                reason=form.cleaned_data.get('reason', '')
            )
            messages.success(request, "คำขอของคุณถูกส่งแล้ว 🎉")
            return redirect('post_detail', pk=target_post.id)
    # แสดงฟอร์มคำขอ (GET request)
    else:
        if post_type == 'swap':
            form = SwapRequestForm(user=request.user)
        elif post_type == 'buy_sell':
            form = SaleRequestForm()
        elif post_type == 'donate':
            form = DonateRequestForm()
        else:
            messages.error(request, "ไม่สามารถสร้างคำขอสำหรับโพสต์ประเภทนี้ได้")
            return redirect('post_detail', pk=target_post.id)

    return render(request, 'requests/request_form.html', {'form': form, 'post': target_post})


@login_required
def request_list(request):
    # แสดงคำขอทั้งหมดที่ส่งมายังโพสต์ของผู้ใช้ที่ล็อกอิน
    requests = Request.objects.filter(post__owner=request.user).order_by('-created_at')
    return render(request, 'requests/request_list.html', {'requests': requests})


@login_required
def my_requests(request):
    # แสดงคำขอทั้งหมดที่ผู้ใช้ที่ล็อกอินเป็นคนส่ง
    my_requests = Request.objects.filter(requester=request.user).order_by('-created_at')
    return render(request, 'requests/my_requests.html', {'my_requests': my_requests})


@login_required
def respond_request(request, request_id, action):
    swap_request = get_object_or_404(Request, id=request_id, post__owner=request.user)

    if action == 'accept':
        swap_request.status = 'accepted'
        # เพิ่ม logic การจัดการเมื่อมีการยอมรับคำขอ
        # เช่น อัปเดตสถานะของโพสต์เป็น "แลกเปลี่ยนแล้ว" หรือ "ขายแล้ว"
    elif action == 'reject':
        swap_request.status = 'rejected'
    
    # ตรวจสอบว่าคำขอถูกตอบรับไปแล้วหรือยัง
    if swap_request.status != 'pending':
        messages.warning(request, "คำขอนี้ได้รับการดำเนินการแล้ว")
    else:
        swap_request.save()
        messages.success(request, f"คำขอถูก {swap_request.get_status_display()} แล้ว")

    return redirect('requests')