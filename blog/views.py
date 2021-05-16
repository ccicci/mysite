from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post

def index(request):
    return render(request, 'index.html', {})

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        # PostForm 안에 post_save()라는 메서드 생성해서 작업
        form = PostForm(request.POST)
        if form.is_valid():
            pass
        post = form.post_save()
        return redirect('post_detail', pk=post.pk)
    return render(request, 'blog/post_edit.html', {'form': PostForm()})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
