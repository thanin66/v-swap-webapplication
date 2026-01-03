import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, PostReport, Swap, BuySell, Donation
from .forms import  DonationForm, PostForm, SwapForm , SaleForm, WishlistForm
from django.core.exceptions import PermissionDenied
from itertools import chain
from django.views.generic import DetailView
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages

form_mapping = {
    'swap': SwapForm,
    'sale': SaleForm,         
    'wishlist': WishlistForm, 
    'donation': DonationForm,
}

from .matching import find_matches_for_user

def post_list(request):
    # แยก QuerySet ส่งไปให้ template
    # 1. สินค้าที่วางขาย (Sale)
    sale_posts = BuySell.objects.filter(is_buying=False).order_by('-created_at')
    
    # 2. รายการที่คนตามหา (Wishlist)
    wishlist_posts = BuySell.objects.filter(is_buying=True).order_by('-created_at')
    
    donation_posts = Donation.objects.all().order_by('-created_at')
    swap_posts = Swap.objects.all().order_by('-created_at')
    
    # Matching Logic (คงเดิมได้เลย เพราะมันใช้ is_buying=True เป็น demand อยู่แล้ว)
    matches_incoming = []
    matches_outgoing = []
    if request.user.is_authenticated:
        matches_incoming, matches_outgoing = find_matches_for_user(request.user)

    context = {
        'sale_posts': sale_posts,
        'wishlist_posts': wishlist_posts, # เพิ่มตัวนี้
        'donation_posts': donation_posts,
        'swap_posts': swap_posts,
        'matches_incoming': matches_incoming,
        # ...
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
    # ตรวจสอบว่า post_type ที่ส่งมามีใน mapping หรือไม่
    if post_type not in form_mapping:
        return redirect('post_list') # หรือ handle error ตามเหมาะสม

    form_class = form_mapping[post_type]

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            
            # --- [ส่วนสำคัญ Logic การแยกประเภท] ---
            if post_type == 'wishlist':
                post.post_type = 'buy_sell' # ใน DB ยังคงเก็บเป็น buy_sell
                post.is_buying = True       # ✅ Flag นี้บอกว่าเป็น Wishlist
            elif post_type == 'sale':
                post.post_type = 'buy_sell'
                post.is_buying = False      # ✅ Flag นี้บอกว่าเป็น การขาย
            else:
                post.post_type = post_type  # swap หรือ donation
            # -----------------------------------
            
            post.save()
            messages.success(request, 'สร้างโพสต์เรียบร้อยแล้ว!')
            return redirect('post_list')
    else:
        form = form_class() 

    return render(request, 'posts/post_form.html', {'form': form, 'post_type': post_type})

    if post_type not in form_mapping:
        return redirect('post_list') # หรือ handle error ตามเหมาะสม


@login_required
def post_edit(request, pk):
    # 1. ดึงข้อมูล Post ตัวแม่มาก่อน
    post = get_object_or_404(Post, pk=pk)
    
    # 2. เช็คว่าเป็นเจ้าของหรือไม่
    if post.owner != request.user:
        raise PermissionDenied("คุณไม่มีสิทธิ์แก้ไขโพสต์นี้")

    # 3. [สำคัญ] แปลง Post ธรรมดา ให้เป็น Object ลูก (Swap, BuySell, Donation) 
    # และเลือก Form ให้ถูกประเภท
    target_post = post # ค่าเริ่มต้น
    form_class = None
    current_post_type_label = post.post_type # เอาไว้ส่งไปบอก Template

    try:
        if post.post_type == 'swap':
            target_post = post.swap  # เข้าถึงตาราง Swap
            form_class = SwapForm
            
        elif post.post_type == 'buy_sell':
            target_post = post.buysell # เข้าถึงตาราง BuySell
            # เช็คว่าเป็น 'ขาย' หรือ 'ตามหา'
            if target_post.is_buying:
                form_class = WishlistForm
                current_post_type_label = 'wishlist'
            else:
                form_class = SaleForm
                current_post_type_label = 'sale'

        elif post.post_type in ['donation', 'donate']:
            target_post = post.donation # เข้าถึงตาราง Donation
            form_class = DonationForm
            
    except Exception as e:
        print(f"Error accessing child object: {e}")
        # กรณีข้อมูลไม่สมบูรณ์ ให้เด้งออกไปก่อน
        return redirect('home')

    # ถ้าหา Form ไม่เจอ (เช่น post_type แปลกๆ)
    if not form_class:
        return redirect('home')

    # 4. Process Form Logic
    if request.method == 'POST':
        # สังเกต: instance ต้องใช้ target_post (ตัวลูก) ไม่ใช่ post (ตัวแม่)
        form = form_class(request.POST, request.FILES, instance=target_post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = form_class(instance=target_post)

    return render(request, 'posts/post_form.html', {
        'form': form,
        'post_type': current_post_type_label, # ส่งค่าที่ถูกต้องไป (sale/wishlist) แทน buy_sell
        'post': target_post,
    })

    
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.owner != request.user:
        raise PermissionDenied("คุณไม่มีสิทธิ์ลบโพสต์นี้")

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