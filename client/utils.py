from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator



def send_email_token(email,token,first_name,user_email):
    try:
        # Build the confirmation URL with the token
        confirmation_url = f'http://127.0.0.1:8000/user/confirm-email/{token}'

        # Send the confirmation email
        subject = ' Subject: Welcome to SMACarRentals! Verify Your Email to Get Started 🚗'
        message = f'''
       
Hello {first_name},

Congratulations on taking the first step towards amazing journeys with SMACarRentals! We're thrilled to have you join our community of travelers and adventurers.

To ensure the security of your account and provide you with a seamless experience, please verify your email address by clicking the link below:

{confirmation_url}

This link will confirm the ownership of your email and give you access to our exceptional car rental services.

Here's how you can proceed:

1. **Sign Up**: You've successfully registered on our platform. If you haven't done so yet, click here to sign up: http://127.0.0.1:8000/user/signup/.

2. **Check Your Inbox**: An email has been sent to the address you provided during registration {user_email}. Can't find the email? Please check your spam or junk folder, just in case.

3. **Click the Verification Link**: Simply click on the link above or copy and paste it into your browser's address bar. This link will verify your email and grant you access to our car rental system.

4. **Access Our Car Rental System**: Once your email is verified, you'll gain full access to our user-friendly car rental platform. Browse through our diverse fleet, make reservations, and manage your bookings with ease.

We understand that your time is valuable, and we're grateful for your commitment to securing your account. Your trust is essential to us, and we're dedicated to providing you with a safe and enjoyable experience.

If you have any questions or need assistance during the email verification process, our dedicated support team is here to help. Reach out to them at [support email/phone number], and they'll be more than happy to assist you.

Thank you for choosing SMACarRental for your travel needs. Get ready to embark on unforgettable journeys and make memories that last a lifetime.

Best regards,

Mohd Ahmad
Developer
SMACarRental
'''
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email,]
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(e)
        return False
    return True
