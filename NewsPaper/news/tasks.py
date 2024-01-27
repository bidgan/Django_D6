from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category
from datetime import datetime, timedelta


@shared_task
def send_email_task(pk):
    post = Post.objects.get(pk=pk)
    categories = post.categories.all()
    title = post.title
    subscribers_emails = []

    for category in categories:
        subscribers_users = category.subscribers.all()
        for sub_user in subscribers_users:
            subscribers_emails.append(sub_user.email)
            
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': f'{post.title}',
            'link': f'{settings.SITE_URL}/news/{pk}/',
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def weekly_send_email_task():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(created_at__gte=last_week)
    categories = posts.values_list('categories__name', flat=True)
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
