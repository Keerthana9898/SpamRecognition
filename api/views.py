from django.contrib.auth import authenticate
from django.db import models
from django.db.models import Case, F, IntegerField, Q, Value, When
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.authentication import CustomUserAuth
from api.models import Global

from .serializers import (CustomUserSerializer, GlobalDbSerializer,
                          SpamSerializer)


class CustomUserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        URL: /api/v1/registeration
        Payload: 
        
        """
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)      
        return Response({"Message": "Error while registering the user", "Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class CustomUserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        if not username or not password:
            return Response({'Message': 'Mandatory fields username/password not present'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'Error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class SpamView(APIView):
    authentication_classes = [CustomUserAuth]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user  = request.user
        data = request.data
        data["reported_by"] = user.id
        serializer = SpamSerializer(data=data)
        if serializer.is_valid():
            spam = serializer.save()
        else:
            return Response({"Message": "Error while marking the number as spam", "Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            global_record = Global.objects.get(phone_number=request.data.get("phone_number"))
            global_record.spam = spam
            global_record.save()
            return Response({"Message": "Marked as spam"}, status=status.HTTP_200_OK)
        except Global.DoesNotExist:
            data["spam"] = spam.id
            if not data.get("name"):
                data["name"] = "Spam user" 
            serializer = GlobalDbSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Message": "Added to global db as spam"}, status=status.HTTP_200_OK)
            return Response({"Message": "Error while adding the spam user to globaldb", "Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class GlobalDbView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = GlobalDbSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)      
        return Response({"Message": "Error while adding the user to globaldb", "Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        type = request.GET.get("type")
        query = request.GET.get("query")
        user_id = request.user.id
        if type == "phone_number":
            results = Global.objects.annotate(
                            match_type=Case(
                                    When(phone_number__iexact=query, then=Value(3)),  # Exact match
                                    When(phone_number__istartswith=query, then=Value(2)),  # Starts with the query
                                    When(phone_number__icontains=query, then=Value(1)),  # Contains the query
                                    default=Value(0),
                                    output_field=IntegerField(),
                            ),
                            spam_likelihood=Case(
                                    When(spam__phone_number=F('phone_number'), then=Value(True)), 
                                    default=Value(False),
                                    output_field=models.BooleanField(),
                            ),
                            ).filter(
                                    Q(phone_number__icontains=query)
                            ).order_by('-match_type', 'name')
            response_data = list(results.values('name', 'phone_number', 'email', 'spam'))
            return Response({"query_data": response_data}, status=status.HTTP_200_OK)
        elif type == "name":
            results = Global.objects.annotate(
                            match_type=Case(
                                    When(name__iexact=query, then=Value(3)),  # Exact match
                                    When(name__istartswith=query, then=Value(2)),  # Starts with the query
                                    When(name__icontains=query, then=Value(1)),  # Contains the query
                                    default=Value(0),
                                    output_field=IntegerField(),
                            ),
                            spam_likelihood=Case(
                                    When(spam__phone_number=F('phone_number'), then=Value(True)), 
                                    default=Value(False),
                                    output_field=models.BooleanField(),
                            ),
                            ).filter(
                                    Q(name__icontains=query)
                            ).order_by('-match_type', 'name')
            response_data = list(results.values('name', 'phone_number', 'email', 'spam'))
            return Response({"query_data": response_data}, status=status.HTTP_200_OK)
        else:
            return Response({"Error": "Invalid query type"}, status=status.HTTP_400_BAD_REQUEST)
        