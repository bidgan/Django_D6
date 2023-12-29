from django.urls import path
from .views import PostsList, PostDetail, home, search_news,NewsList, ArticlesList,PostCreate,PostUpdate,PostDelete
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Домашняя страница с ссылками на новости и статьи
    path('news/', NewsList.as_view(), name='news-list'),
    path('news/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('news/search', search_news, name='search_news'),
    path('news/create/', PostCreate.as_view(), name='post_create'),
    path('news/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    # Представления для статей
    path('articles/', ArticlesList.as_view(), name='articles-list'),
    path('articles/create/', PostCreate.as_view(), name='post_create'),
    path('articles/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('articles/search', search_news, name='search_news'),
    path('articles/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]
