from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import BuySellForm, DonationForm, PostForm, SwapForm

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})

@login_required
def post_type_select(request):
    return render(request, 'posts/post_type_select.html')

@login_required
def post_create(request, post_type):
    if post_type == 'swap':
        form_class = SwapForm
    elif post_type == 'buy_sell':
        form_class = BuySellForm
    elif post_type == 'donation':
        form_class = DonationForm
    else:
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

    return render(request, 'posts/post_form.html', {'form': form, 'post_type': post_type})
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, owner=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_form.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, owner=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, owner=request.user)
    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})