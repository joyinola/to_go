#sends otp to email
import pyotp


from django.utils.encoding import (
    smart_str,
    smart_bytes,
    force_str,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.template.loader import get_template
from django.core.mail import send_mail

secret = pyotp.random_base32()
totp = pyotp.TOTP(secret, interval=60)


def send_otp(user):
    """
    Send One time password to user


    """
    user_name = f"{user.first_name} {user.last_name}"
    otp = totp.at(for_time=user.created_at) 
  
    subject = "OTP For TO-GO app"
    email_body = f"""
    Below is your One-Time password
    {otp}
    """
    context = {"user_name": user_name, "otp": otp}
    try:
        send_mail(
            subject=subject,
            message=email_body,
            from_email=None,
            html_message=get_template("rider/otp.html").render(context),
            recipient_list=[user.email],
            fail_silently=False,
        )
        return otp
    except Exception as exception:
        return False
    
def verify_otp(user,otp):
    return totp.verify(otp,user.created_at,valid_window=60)







#send resetpasswordurl functions
def encode_user_id(id):
    uuid_encoded = urlsafe_base64_encode(smart_bytes(id))
    return uuid_encoded


def decode_user_id(uuid_encoded):
    try:
        uuid_decoded = force_str(urlsafe_base64_decode(uuid_encoded))
        return uuid_decoded
    except:
        return None


def password_reset_token_is_valid(user, token):
    if PasswordResetTokenGenerator().check_token(user, token):
        return True
    else:
        return False


def generate_password_reset_url(user, request):
    """
    Generate the password reset url
    """
    user_id_encoded = encode_user_id(user.id)
    token = PasswordResetTokenGenerator().make_token(user)

    # current_site= get_current_site(request).domain
    # domain = current_site.split(":")
    base_url = "localhost:8000"

  

    relative_link = f"reset_password/{str(token)}/{user_id_encoded}"
    absolute_url = f"http://{base_url}/{relative_link}"

    return absolute_url


def send_password_reset_email(user, request):
    """
    Send password reset email to the recipient.

    """
    user_name = f"{user.first_name} {user.last_name}"
    absolute_url = generate_password_reset_url(user, request)
    subject = "Reset your account password"
    email_body = f"""
    Use the link below to reset your password.
    {absolute_url}
    """
    context = {"user_name": user_name, "absolute_url": absolute_url}
    try:
        send_mail(
            subject=subject,
            message=email_body,
            from_email=None,
            html_message=get_template("rider/password_reset.html").render(context),
            recipient_list=[user.email],
            fail_silently=False,
        )
        return True
    except Exception as exception:
        return False
