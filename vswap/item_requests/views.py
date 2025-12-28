# requests/views.py
from django.http import HttpResponseForbidden, JsonResponse
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

    return render(request, 'item_requests/request_form.html', {'form': form, 'post': target_post})



@login_required
def respond_request(request, request_id, action):
    swap_request = get_object_or_404(Request, id=request_id, post__owner=request.user)
    if request.user not in [swap_request.requester, swap_request.post.owner]:
        return JsonResponse({"error": "permission denied"}, status=403)
    if swap_request.status != 'pending':
        messages.warning(request, "คำขอนี้ได้รับการดำเนินการแล้ว")
        return redirect('request_page')

    if action == 'accept':
        swap_request.status = 'accepted'
    elif action == 'reject':
        swap_request.status = 'rejected'
    else:
        messages.error(request, "คำสั่งไม่ถูกต้อง")
        return redirect('request_page')

    swap_request.save()
    messages.success(request, f"คุณได้ {swap_request.get_status_display()} คำขอแล้ว")

    return redirect('request_page')

@login_required
def request_page(request):
    my_requests = Request.objects.filter(
        requester=request.user
    ).order_by('-created_at')

    incoming_requests = Request.objects.filter(
        post__owner=request.user
    ).order_by('-created_at')

    return render(request, 'item_requests/requests_page.html', {
        'my_requests': my_requests,
        'incoming_requests': incoming_requests,
    })


@login_required
def get_accept_status(request, request_id):
    swap_request = get_object_or_404(Request, id=request_id)
    if request.user not in [swap_request.requester, swap_request.post.owner]:
        return JsonResponse({"error": "permission denied"}, status=403)
    
    # ใครเป็นใคร
    if request.user == swap_request.requester:
        my_status = swap_request.user1_status
        other_status = swap_request.user2_status
    else:
        my_status = swap_request.user2_status
        other_status = swap_request.user1_status

    both_accepted = (
        swap_request.user1_status == "accepted" and 
        swap_request.user2_status == "accepted"
    )

    return JsonResponse({
        "my_status": my_status,
        "other_status": other_status,
        "done": both_accepted
    })

@login_required
def submit_accept(request, request_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    swap_request = get_object_or_404(Request, id=request_id)
    if request.user not in [swap_request.requester, swap_request.post.owner]:
        return JsonResponse({"error": "permission denied"}, status=403)
    
    if request.user == swap_request.requester:
        swap_request.user1_status = "accepted"
    else:
        swap_request.user2_status = "accepted"

    # เช็คว่าทั้งคู่กดยืนยันแล้ว
    if swap_request.user1_status == "accepted" and swap_request.user2_status == "accepted":
        swap_request.status = "accepted"

    swap_request.save()
    return JsonResponse({"ok": True})

@login_required
def cancel_accept(request, request_id):
    swap_request = get_object_or_404(Request, id=request_id)
    if request.user not in [swap_request.requester, swap_request.post.owner]:
        return JsonResponse({"error": "permission denied"}, status=403)
    # reset ทั้งคู่กลับไป pending
    swap_request.user1_status = "pending"
    swap_request.user2_status = "pending"
    swap_request.save()

    return JsonResponse({"ok": True})
login_required
def cancel_request(request, request_id):
    swap_request = get_object_or_404(Request, id=request_id)
    if request.user not in [swap_request.requester, swap_request.post.owner]:
        return JsonResponse({"error": "permission denied"}, status=403)
    swap_request.status = 'pending'
    swap_request.save()
    messages.success(request, "คุณได้ยกเลิกคำขอเรียบร้อยแล้ว")
    return redirect('request_page')


@login_required
def request_confirm(request, request_id):
    swap_request = get_object_or_404(Request, id=request_id)
    
    if request.user not in [swap_request.requester, swap_request.post.owner]:
        return JsonResponse({"error": "permission denied"}, status=403)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'confirm_user1':
            swap_request.user1_status = 'accepted'
        elif action == 'confirm_user2':
            swap_request.user2_status = 'accepted'
        swap_request.save()

        # ตรวจสอบว่าทั้งสองฝ่ายยืนยันแล้วหรือไม่
        if swap_request.user1_status == 'accepted' and swap_request.user2_status == 'accepted':
            swap_request.status = 'accepted'
            swap_request.save()
            messages.success(request, "การแลกเปลี่ยนเสร็จสมบูรณ์ 🎉")
            return redirect('request_page')

        messages.success(request, "คุณได้ยืนยันคำขอแล้ว รออีกฝ่ายยืนยัน")
        return redirect('request_page')

    return render(request, 'item_requests/request_confirm.html', {'swap_request': swap_request})



@login_required
def request_map_confirm(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    if request.user not in [req.requester, req.post.owner]:
        return JsonResponse({"error": "permission denied"}, status=403)

    return render(request, "item_requests/request_map_confirm.html", {"req": req})

@login_required
def api_map_status(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    if request.user not in [req.requester, req.post.owner]:
        return JsonResponse({"error": "permission denied"}, status=403)

    if request.user == req.requester:
        my_confirmed = req.user1_position_confirmed
        other_confirmed = req.user2_position_confirmed
    else:
        my_confirmed = req.user2_position_confirmed
        other_confirmed = req.user1_position_confirmed

    return JsonResponse({
        "my_confirmed": my_confirmed,
        "other_confirmed": other_confirmed,
        "lat": req.position_lat,
        "lng": req.position_lng
    })


@login_required
def api_submit_map_position(request, request_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    
    req = get_object_or_404(Request, id=request_id)
    if request.user not in [req.requester, req.post.owner]:
        return JsonResponse({"error": "permission denied"}, status=403)

    lat = float(request.POST.get("lat"))
    lng = float(request.POST.get("lng"))

    position_changed = (req.position_lat != lat) or (req.position_lng != lng)
    req.position_lat = lat
    req.position_lng = lng

    if position_changed:
        req.user1_position_confirmed = False
        req.user2_position_confirmed = False

    if request.user == req.requester:
        req.user1_position_confirmed = True
    else:
        req.user2_position_confirmed = True

    req.save()

    return JsonResponse({"ok": True, "reset": position_changed})

@login_required
def next_step(request, request_id):
    swap_request = get_object_or_404(Request, id=request_id)

    post = swap_request.post
    offered_post = swap_request.offered_product

    return render(request, "item_requests/next_step.html", {
        "request_obj": swap_request,
        "post": post,
        "offered_post": offered_post,
    })

@login_required
def update_multiple_post_status(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        post_ids = request.POST.get('post_ids', '') 
        ids = [int(pk) for pk in post_ids.split(',') if pk.isdigit()]

        for pk in ids:
            post = get_object_or_404(Post, id=pk)
            post.status = status
            post.save()

    return redirect('home')