from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import CustomUser


class CustomUserAuth:
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is not None and password is not None:
            try:
                user = CustomUser.objects.get(username=username)
                if user.check_password(password):
                    return user
            except CustomUser.DoesNotExist:
                return None
        
        elif request.headers and 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                access_token = auth_header.split(' ')[1]
                try:
                    token = AccessToken(access_token)
                    user_id = token['user_id']
                    user = CustomUser.objects.get(id=user_id)
                    return user, None
                except CustomUser.DoesNotExist:
                    raise AuthenticationFailed('User does not exist')
                except Exception as e:
                    raise AuthenticationFailed('Token authentication failed: {}'.format(str(e)))
        
        return None


    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
        
    def authenticate_header(self, request):
        pass
