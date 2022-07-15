from django.contrib.auth.signals import user_logged_out, user_login_failed
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.contrib import messages


# @receiver(user_logged_out, sender=User)
def log_out(sender, request, user, **kwargs):
    print("decorator called")
    messages.add_message(request, messages.SUCCESS, message="Logged out successfully.")


user_logged_out.connect(log_out, sender=User)
