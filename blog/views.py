from django.shortcuts import render, get_object_or_404, redirect 
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def post_index(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_index.html', {'posts': posts})
    
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)
       
    form = CommentForm()
    if request.method == "POST": 
        form = CommentForm(request.POST)
        if not request.user.is_authenticated:
            return redirect('login')        
        if form.is_valid():
            comment = Comment(
                user=form.cleaned_data["user"],
                text=form.cleaned_data["text"],
                post=post,
            )
            comment.save()

    context = {"post": post, "comments": comments, "form": form}
    return render(request, "blog/post_detail.html", context)
    
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
    
@login_required
def post_edit(request, pk):
    
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            #post.author == request.user
#        if request.user == post.author:
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})    
    
@login_required    
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.author = request.user
    post.delete()
    return redirect('post_index') 
    
    
def post_category(request, category):
        
    if category:
        posts = Post.objects.filter(categories__name__contains=category).order_by(
        "-created_date"
    )  
    return render(request, 'blog/post_index.html', {'category': category,'posts': posts})    
    
    
    
@login_required    
def dashboard(request):
    user = request.user
    
    user_posts = Post.objects.filter(author=request.user).order_by('-published_date')

    template = 'blog/dashboard.html'
    context = {
    
    "posts": user_posts
    
  }

    return render(request, template, {'user_posts':user_posts, 'user': user})
    