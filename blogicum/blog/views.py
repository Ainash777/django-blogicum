from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .forms import CommentForm

from .models import Post, Category, Location, Comment
from .forms import PostForm, CommentForm


def index(request):
    """Главная страница со всеми постами"""
    # Получаем ВСЕ опубликованные посты
    post_list = Post.objects.filter(is_published=True)

    # Создаем пагинатор: 10 постов на страницу
    paginator = Paginator(post_list, 10)

    # Получаем номер страницы из GET-параметра
    page_number = request.GET.get('page')

    # Получаем объект страницы
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/index.html', {'page_obj': page_obj})


@login_required
def add_comment(request, post_id):
    """Добавление комментария к посту"""
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

    # Всегда перенаправляем обратно на пост
    return redirect('blog:post_detail', post_id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    """Редактирование комментария"""
    # Используем post__id вместо post_id
    comment = get_object_or_404(Comment, id=comment_id, post__id=post_id)

    # Проверяем, что пользователь - автор комментария
    if comment.author != request.user:
        return HttpResponseForbidden("Вы не автор этого комментария")

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post_id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/edit_comment.html', {
        'form': form,
        'post_id': post_id,
        'comment': comment,
    })


@login_required
def post_delete(request, post_id):
    """Удаление поста"""
    post = get_object_or_404(Post, id=post_id)

    # Проверяем, что пользователь - автор поста
    if post.author != request.user:
        return HttpResponseForbidden("Вы не автор этого поста")

    if request.method == 'POST':
        # Удаляем пост
        post.delete()
        # Перенаправляем на профиль пользователя
        return redirect('blog:profile', username=request.user.username)

    # Для GET запроса показываем страницу подтверждения
    return render(request, 'blog/confirm_delete.html', {
        'object': post,
        'object_type': 'пост',
        'back_url': 'blog:post_detail',
        'back_id': post.id,
    })


@login_required
def comment_delete(request, post_id, comment_id):
    """Удаление комментария"""
    comment = get_object_or_404(Comment, id=comment_id)

    # Проверяем, что комментарий относится к этому посту
    if comment.post.id != post_id:
        return HttpResponseForbidden("Комментарий не относится к этому посту")

    # Проверяем, что пользователь - автор комментария
    if comment.author != request.user:
        return HttpResponseForbidden("Вы не автор этого комментария")

    if request.method == 'POST':
        # Удаляем комментарий
        comment.delete()
        # Перенаправляем обратно на пост
        return redirect('blog:post_detail', post_id=post_id)

    # Для GET запроса показываем страницу подтверждения
    return render(request, 'blog/confirm_delete.html', {
        'object': comment,
        'object_type': 'комментарий',
        'back_url': 'blog:post_detail',
        'back_id': post_id,
    })
@login_required
def post_create(request):
    """Создание нового поста"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Автор = текущий пользователь
            post.save()
            # Перенаправляем на профиль пользователя
            return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm()

    categories = Category.objects.all()
    locations = Location.objects.all()

    return render(request, 'blog/create.html', {
        'form': form,
        'categories': categories,
        'locations': locations,
        'editing': False,  # Флаг для шаблона - не редактирование
    })


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()  # Получаем все комментарии к посту

    comment_form = CommentForm()  # Пустая форма для комментария

    return render(request, 'blog/detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })
@login_required
def post_edit(request, post_id):
    """Редактирование поста"""
    # Получаем пост
    post = get_object_or_404(Post, id=post_id)

    # Проверяем, что пользователь - автор поста
    if post.author != request.user:
        return HttpResponseForbidden("Вы не автор этого поста")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    categories = Category.objects.all()
    locations = Location.objects.all()

    return render(request, 'blog/create.html', {
        'form': form,
        'post': post,
        'categories': categories,
        'locations': locations,
        'editing': True,
    })
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # ЭТА СТРОКА ДЛЯ ПЕРЕНАПРАВЛЕНИЯ НА ПРОФИЛЬ:
            return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm()

    categories = Category.objects.all()
    locations = Location.objects.all()

    return render(request, 'blog/create.html', {
        'form': form,
        'categories': categories,
        'locations': locations,
        'editing': False,
    })


def profile(request, username):
    """Профиль пользователя"""
    # Получаем пользователя по username
    user = get_object_or_404(User, username=username)

    # Получаем все посты этого пользователя
    posts = Post.objects.filter(author=user).order_by('-pub_date')

    # Пагинация для постов в профиле (10 на странице)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/profile.html', {
        'profile_user': user,
        'page_obj': page_obj,
    })