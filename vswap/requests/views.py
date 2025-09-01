from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from posts.models import Post, Swap  # Correct relative import
from .models import Request

@login_required
def send_request(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            swap_request = Request.objects.create(
                post=post,
                message=message,
                requester=request.user
            )
            messages.success(request, "คำขอของคุณถูกส่งแล้ว 🎉")
            return redirect('post_detail', pk=post.id)
    return render(request, 'requests/request_form.html', {'post': post})


@login_required
def request_list(request):
    requests = Request.objects.filter(post__owner=request.user).order_by('-created_at')
    return render(request, 'requests/request_list.html', {'requests': requests})

@login_required
def my_requests(request):
    my_requests = Request.objects.filter(requester=request.user).order_by('-created_at')
    return render(request, 'requests/my_requests.html', {'my_requests': my_requests})

@login_required
def respond_request(request, request_id, action):
    swap_request = get_object_or_404(Request, id=request_id, post__owner=request.user)

    if action == 'accept':
        swap_request.status = 'accepted'
    elif action == 'reject':
        swap_request.status = 'rejected'

    swap_request.save()
    return redirect('requests')