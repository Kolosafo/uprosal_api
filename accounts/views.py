from django.shortcuts import render

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# Create your views here.
from .models import User, UserToken, Reset
from .serializers import UserSerializer
from .auth import create_access_token, authenticate, create_refresh_token, decode_refresh_token
import datetime
from django.core.mail import send_mail
import secrets
from django.http import Http404
import json
import io

from django.http import JsonResponse, HttpResponse
from rest_framework import exceptions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
from datetime import datetime, timezone, date
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def register(request):
    data = request.data

    if data['password'] != data['password_confirm']:
        raise exceptions.APIException('Passwords do not match!')

    serializer = UserSerializer(data=data)
    if serializer.is_valid():

        serializer.is_valid(raise_exception=True)
        serializer.save()
    else:
        print(serializer.errors)
        return Response("already exists", status=status.HTTP_409_CONFLICT)

    return Response("successs")


@api_view(['POST'])
def login(request):
    email = request.data['email']
    password = request.data['password']

    user = User.objects.filter(email=email).first()

    if user is None:
        raise exceptions.AuthenticationFailed('Invalid credentials')

    if not user.password == password:
        print(user.password, "USER PASSWORD")
        print(password, "USER PASSWORD")
        raise exceptions.AuthenticationFailed("invalid credentials")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    # UserToken.objects.create(user_id=user.id, token=refresh_token,
    #                          expired_at=datetime.utcnow() + datetime.timedelta(days=7))

    response = Response()

    response.set_cookie(key='refresh_token',
                        value=refresh_token, httponly=True)
    response.data = {
        'token': access_token
    }

    return response


@api_view(['GET'])
def user(request):
    try:
        authentication_class = authenticate(request)
    except Exception as E:
        print("ERROR", get_authorization_header(request))

    return Response(UserSerializer(authenticate(request)).data)


@api_view(['POST'])
def refresh(request):
    refresh_token = request.COOKIES.get('refresh_token')
    id = decode_refresh_token(refresh_token)

    if not UserToken.objects.filter(
        user_id=id,
        token=refresh_token,
        expired_at__gt=datetime.datetime.now(tz=datetime.timezone.utc)
    ).exists():
        raise exceptions.AuthenticationFailed("Unathenticated")

    access_token = create_access_token(id)

    return Response({'token': access_token})


@api_view(['POST'])
def logout(request):
    # authenticate(request)
    refresh_token = request.COOKIES.get('refresh_token')
    UserToken.objects.filter(token=refresh_token).delete()
    response = Response()
    response.delete_cookie(key='refresh_token')
    response.data = {
        'message': 'success'
    }
    return response


@api_view(['POST'])
def password_reset(request):
    data = request.data

    if data['password'] != data['password_confirm']:
        raise exceptions.APIException('Passwords do not match!')

    reset_password = Reset.objects.filter(token=data['token']).first()
    if not reset_password:
        raise exceptions.APIException("Invalid link!")

    user = User.objects.filter(email=reset_password.email).first()

    if not user:
        raise exceptions.APIException("User not found!")

    user.set_password(data['password'])
    user.save()

    return Response({
        'message': 'success'
    })
