from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.conf import settings


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author')
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    # Добавляем метод __str__
    def __str__(self):
        return self.user.get_full_name() or self.user.username

    def update_rating(self):
        # Суммарный рейтинг статей автора, умноженный на 3
        rating_posts = sum(post.rating for post in self.post_set.all()) * 3
        # Суммарный рейтинг комментариев автора
        rating_comments = sum(comment.rating for comment in Comment.objects.filter(user=self.user))
        # Суммарный рейтинг комментариев к статьям автора
        rating_comments_posts = sum(comment.rating for post in self.post_set.all() for comment in post.comments.all())

        # Обновление общего рейтинга автора
        self.rating = rating_posts + rating_comments + rating_comments_posts
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    POST_TYPES = [
        (NEWS, 'News'),
        (ARTICLE, 'Article')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=ARTICLE)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255, default='Default title', verbose_name='Заголовок')
    content = models.CharField(max_length=2048, default='default content', verbose_name='Контент')
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.title.title()}: {self.content[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
