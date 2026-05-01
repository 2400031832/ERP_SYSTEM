from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


class VercelCookieAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            user_pk = request.get_signed_cookie('erp_user_id', default=None, salt='erp-auth')
            if user_pk:
                try:
                    request.user = get_user_model().objects.get(pk=user_pk, is_active=True)
                except get_user_model().DoesNotExist:
                    request.user = AnonymousUser()

        return self.get_response(request)
