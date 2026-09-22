from django.shortcuts import render, get_object_or_404
from .models import Post

def news_list(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'blog/news_list.html', {'posts': posts})

def news_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/news_detail.html', {'post': post})