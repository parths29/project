import os
from iBlogger.celery import app
from .models import Subscriber, Account
from django.core.mail import send_mail
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iBlogger.settings')

FROM_EMAIL = settings.EMAIL_HOST_USER
EMAIL_PASSWORD = settings.EMAIL_HOST_PASSWORD
DOMAIN_NAME = settings.DOMAIN_NAME


@app.task()
def send_emails(author, slug):
    author_name = Account.objects.get(id=author)
    subscribers = Subscriber.objects.filter(following_user_id=author)
    link = f"http://{DOMAIN_NAME}:8000/blogpost/{slug}"
    email_list = []
    for subscriber in subscribers:
        user = Account.objects.get(username=subscriber.follower_user_id)
        email_list.append(user.email)
    send_mail(
        subject=f"New post from {author_name}.",
        message=f"Hello,\n\nyour following {author_name} has added a new post.\n\nCheck it out at {link}",
        from_email=FROM_EMAIL,
        recipient_list=email_list,
        fail_silently=True
    )


@app.task()
def send_verification_code(unique_id, verification_code, email):
    link = f"http://{DOMAIN_NAME}:8000/verification/{unique_id}/{verification_code}"
    send_mail(
        subject="Email verification for iBlogger",
        message=f"Hello,\nYour account has been created. Please verify your email. {link}",
        from_email=FROM_EMAIL,
        recipient_list=[email],
    )


@app.task()
def send_password_reset_link(unique_id, email, password_reset_code):
    link = f"http://{DOMAIN_NAME}:8000/reset_password/{unique_id}/{password_reset_code}"
    send_mail(
        subject="Password reset link for iBlogger",
        message=f"Hello,\nPlease go to the link to reset your account password. {link}",
        from_email=FROM_EMAIL,
        recipient_list=[email],
    )
