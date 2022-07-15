import os
from iBlogger.celery import app
from .models import Subscriber, Account
from django.core.mail import send_mail
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iBlogger.settings')

FROM_EMAIL = settings.EMAIL_HOST_USER
EMAIL_PASSWORD = settings.EMAIL_HOST_PASSWORD


@app.task()
def send_emails(author, slug):
    author_name = Account.objects.get(id=author)
    subscribers = Subscriber.objects.filter(following_user_id=author)
    link = f"http://127.0.0.1:8000/blogpost/{slug}"
    email_list = []
    for subscriber in subscribers:
        user = Account.objects.get(username=subscriber.follower_user_id)
        # print(user.email)
        email_list.append(user.email)
    # print(email_list)
    send_mail(
        subject=f"New post from {author_name}.",
        message=f"Hello,\n\nyour following {author_name} has added a new post.\n\nCheck it out at {link}",
        from_email=FROM_EMAIL,
        recipient_list=email_list,
        fail_silently=True
    )
