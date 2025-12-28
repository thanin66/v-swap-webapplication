import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, PostReport, Swap, BuySell, Donation
from .forms import BuySellForm, DonationForm, PostForm, SwapForm
from itertools import chain
from django.views.generic import DetailView
from django.db.models import Q
from django.urls import reverse

form_mapping = {
    'swap': SwapForm,
    'buy_sell': BuySellForm,
    'donation': DonationForm,
}

from .matching import find_matches_for_user

def post_list(request):
    buysell_posts = BuySell.objects.all()
    donation_posts = Donation.objects.all()
    swap_posts = Swap.objects.all()
    
    all_posts = sorted(
        chain(buysell_posts, donation_posts, swap_posts),
        key=lambda x: x.created_at,
        reverse=True
    )
    
    # --- [ส่วนที่ต้องเพิ่ม] ---
    matches_incoming = []
    matches_outgoing = []
    
    # ตรวจสอบว่าล็อกอินหรือยัง ก่อนเรียกใช้ AI
    if request.user.is_authenticated:
        matches_incoming, matches_outgoing = find_matches_for_user(request.user)
    # -----------------------

    context = {
        'posts': all_posts,
        # ส่งตัวแปรแมทช์ไปที่หน้าเว็บ
        'matches_incoming': matches_incoming, 
        'matches_outgoing': matches_outgoing,
    }
    
    return render(request, 'posts/post_list.html', context)
class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'  

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg or 'pk')
        post = get_object_or_404(Post, pk=pk)

        try:
            if post.post_type == 'swap':
                return Swap.objects.get(pk=pk)
            if post.post_type == 'buy_sell':
                return BuySell.objects.get(pk=pk)
            if post.post_type == 'donate':
                return Donation.objects.get(pk=pk)
        except (Swap.DoesNotExist, BuySell.DoesNotExist, Donation.DoesNotExist):
            return post

        return post
    

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
        'post': post,
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

def map_view(request):
    # ดึงโพสต์ทั้งหมดที่มี lat/lng
    posts_qs = Post.objects.exclude(leaflet_lat__isnull=True, leaflet_lng__isnull=True)
    
    # แปลงเป็น list ของ dict และรวม post_type
    posts = list(posts_qs.values('id', 'title', 'description', 'leaflet_lat', 'leaflet_lng', 'post_type'))
    
    return render(request, 'posts/map.html', {'posts': posts})


def search_view(request):
    try:
        q = request.GET.get("q", "").strip()
        
        # 1. ถ้าคำค้นหาสั้นเกินไป ให้คืนค่าว่าง
        if len(q) < 2:
            return JsonResponse([], safe=False)

        # 2. ค้นหาข้อมูล (ใช้ object เต็มๆ ป้องกัน error เรื่อง field หาย)
        posts = Post.objects.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(owner__username__icontains=q)
        ).select_related('owner').order_by('-created_at')[:10]

        data = []
        for post in posts:
            # 3. จัดการรูปภาพแบบปลอดภัย (ถ้าไม่มีรูป ให้ใช้รูป default)
            if post.image:
                image_url = post.image.url
            else:
                image_url = "https://t4.ftcdn.net/jpg/05/97/47/95/360_F_597479556_7bbQ7t4Z8k3xbAloHFHVdZIizWK1PdOo.jpg"

            # 4. สร้าง JSON Response
            data.append({
                "id": post.id,
                "title": post.title,
                "type": post.get_post_type_display(), # แปลง post_type เป็นชื่อภาษาไทย
                "owner": post.owner.username,
                "url": reverse('post_detail', args=[post.id]),
                "image": image_url,

                "lat": post.leaflet_lat, 
                "lng": post.leaflet_lng,
            })
            
        return JsonResponse(data, safe=False)

    except Exception as e:
        # ถ้ามี Error ให้แสดงใน Console ของ Server แทนที่จะเงียบไป
        print(f" Search Error: {e}")
        return JsonResponse([], safe=False)
    

def search_page(request):
    query = request.GET.get('q', '')
    posts = []

    if query:
        # ใช้ Logic การค้นหาเดียวกับ API แต่ไม่ต้องแปลงเป็น Dictionary
        # ค้นหาจาก Title, Description และชื่อเจ้าของโพสต์
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(owner__username__icontains=query)
        ).select_related('owner').order_by('-created_at')
    
    context = {
        'posts': posts,
        'query': query,
    }
    return render(request, 'posts/search_results.html', context)

@login_required
def report_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        reason = request.POST.get("reason", "")
        already_reported = PostReport.objects.filter(post=post, reporter=request.user).exists()
        if not already_reported and reason:

            if reason:
                PostReport.objects.create(
                    post=post,
                    reporter=request.user,
                    reason=reason
                )
                return redirect('post_detail', pk=post.pk)
        else:
            print("User has already reported this post or reason is empty.")

    return redirect('post_detail', pk=post.pk)