from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import CustomUser


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token

    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
            user = CustomUser.objects.get(pk=user_id)
            return user
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('User not found', code='user_not_found')
        except KeyError:
            raise AuthenticationFailed('Invalid token', code='invalid_token')
