from django.core.mail import send_mail
from django.conf import settings
def send_account_verification_mail(email_token,email):
    subject='Your Account Verification Mail' 
    from_email=settings.EMAIL_HOST_USER
    message=f'Hi Click on this link to activate your account http://127.0.0.1:8000/accounts/login/{email_token}'
    send_mail(subject,message,from_email,[email])