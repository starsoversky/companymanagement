from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

User = get_user_model()


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Activate user account
        user.email_is_verified = True
        user.save()
        # Redirect to a success page or login page
        return HttpResponse(
            "Thank you for registering. Your inquiry will be answered soon"
        )  # Replace 'login' with the name of your login URL pattern
    else:
        # Activation link is invalid
        return HttpResponse(
            "Something is wrong"
        )  # Render a template indicating activation failure
