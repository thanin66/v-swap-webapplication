from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Swap, BuySell, Donation
from .forms import BuySellForm, DonationForm, PostForm, SwapForm
from itertools import chain
from django.views.generic import DetailView

form_mapping = {
    'swap': SwapForm,
    'buy_sell': BuySellForm,
    'donation': DonationForm,
}


def post_list(request):
    buysell_posts = BuySell.objects.all()
    donation_posts = Donation.objects.all()
    swap_posts = Swap.objects.all()
    
    # รวม QuerySets ทั้งหมดเข้าด้วยกัน
    all_posts = sorted(
        chain(buysell_posts, donation_posts, swap_posts),
        key=lambda x: x.created_at,
        reverse=True
    )   
    # เรียงลำดับตามวันที่สร้าง (created_at) จากใหม่ไปเก่า
    all_posts.sort(key=lambda x: x.created_at, reverse=True)
    
    return render(request, 'posts/post_list.html', {'posts': all_posts})


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'


@login_required
def post_create(request, post_type):
    form_class = form_mapping.get(post_type)
    if not form_class:
        return redirect('home')

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = form_class()

    return render(request, 'posts/post_form.html', {
        'form': form,
        'post_type': post_type,
    })


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, owner=request.user)
    form_class = form_mapping.get(post.post_type)
    if not form_class:
        return redirect('home')

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = form_class(instance=post)

    return render(request, 'posts/post_form.html', {
        'form': form,
        'post_type': post.post_type,
    })

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, owner=request.user)
    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})

@login_required
def send_request(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        # Logic to handle sending request (e.g., sending email or notification)
        return redirect('post_detail', pk=post.pk)
    return render(request, 'posts/send_request.html', {'post': post})