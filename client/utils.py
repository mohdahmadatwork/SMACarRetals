from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator



def send_email_token(email,token):
    try:
        # Build the confirmation URL with the token
        confirmation_url = f'http://127.0.0.1:8000/user/confirm-email/{token}'

        # Send the confirmation email
        subject = 'Confirm your email address'
        message = f'Click the following link to confirm your email address: {confirmation_url}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email,]
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(e)
        return False
    return True
