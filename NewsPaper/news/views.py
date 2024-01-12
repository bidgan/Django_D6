from django.shortcuts import render
from datetime import datetime
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Post
from .filters import PostFilter
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from news.forms import PostForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


def home(request):
    return render(request, 'home.html')


def news(request):
    return render(request, 'news.html')


def article(request):
    return render(request, 'articles.html')


class PostsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        # Получаем тип поста из контекста, если он задан
        post_type = self.extra_context.get('post_type') if self.extra_context else None
        queryset = super().get_queryset()
        if post_type:  # Если тип поста передан, фильтруем по нему
            queryset = queryset.filter(post_type=post_type)
        self.filterset = PostFilter(self.request.GET, queryset)  # Фильтруем через наш PostFilter
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_exam = Post.objects.all()
        paginator = Paginator(list_exam, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            file_posts = paginator.page(page)
        except PageNotAnInteger:
            file_posts = paginator.page(1)
        except EmptyPage:
            file_posts = paginator.page(paginator.num_pages)

        context['posts'] = file_posts
        return context


class NewsList(PostsList):
    template_name = 'news.html'  # Укажите путь к вашему шаблону для новостей

    def get_queryset(self):
        return super().get_queryset().filter(post_type=Post.NEWS)


class ArticlesList(PostsList):
    template_name = 'articles.html'  # Укажите путь к вашему шаблону для статей

    def get_queryset(self):
        return super().get_queryset().filter(post_type=Post.ARTICLE)


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'


class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.add_post',)


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.change_post',)

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        # Предполагаем, что у модели Author есть связь user, которая указывает на модель User
        if post.author.user != request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


def search_news(request):
    news_list = Post.objects.all()
    news_filter = PostFilter(request.GET, queryset=news_list)
    return render(request, 'search.html', {'filter': news_filter})

class PostDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')
    permission_required = ('news.delete_post',)  # замените 'newspaper' на название вашего приложения

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        # Проверить, связан ли текущий пользователь с автором поста
        if post.author.user != request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

