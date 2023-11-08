from zenithcare_backend import settings
from django.core.mail import send_mail,EmailMessage
from celery import shared_task
from authentification.models import User  # Import your User model

# @shared_task()
def send_otp_email(user_id, otp):
    user = User.objects.get(id=user_id)
    print(user,otp,'------>>>>>>><<<<<<<<-------')
    esubject = "OTP Login"
    emessage = f"Hello {user.username}, your OTP for registration is: {otp}"
    email = EmailMessage(
        esubject,
        emessage,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    print(email,'-------------------')
    email.fail_silently = True
    email.send()

@shared_task()
def send_email_user(user_id):
    user = User.objects.get(id=user_id)
    print(user,'------>>>>>>><<<<<<<<-------')
    esubject = "OTP Login"
    emessage = f"Hello {user.username}, your name is defined through mace and bucket"
    email = EmailMessage(
        esubject,
        emessage,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    print(email,'-------------------')
    email.fail_silently = True
    email.send()
