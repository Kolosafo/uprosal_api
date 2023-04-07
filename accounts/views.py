from django.shortcuts import render

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# Create your views here.
from .models import User, UserToken, Reset, UserQouta
from .serializers import UserSerializer, QoutaSerializer
from .auth import create_access_token, authenticate, create_refresh_token, decode_refresh_token
from django.conf import settings
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
from django.core.mail import send_mail
from django.conf import settings


subscriptionTypes = {
    "Not activated": "Not activated",
    "trial": "trial",
    "Pro": "Pro",
    "Business": "Business",
    "Enterprise": "Enterprise"

}
API_KEY = settings.APIKEY


@api_view(['POST'])
def testEmail(request):
    if not request.headers["Authorization"] == API_KEY:
        return Response("NOT AUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)
    data = request.data
    print(request.headers["Authorization"])
    return Response("request")


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['work_category'] = user.work_category
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def register(request):
    if not request.headers["Authorization"] == API_KEY:
        return Response("NOT AUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)

    data = request.data

    if data['password'] != data['password_confirm']:
        raise exceptions.APIException('Passwords do not match!')

    serializer = UserSerializer(data=data)
    if serializer.is_valid():

        serializer.is_valid(raise_exception=True)
        serializer.save()
        url = 'https://uprosal.com/confirm_email/'+data["email"]
        send_mail("Confirm Your Email", url, settings.EMAIL_HOST_USER, [
            data["email"]], fail_silently=False)
    else:
        print(serializer.errors)
        return Response("already exists", status=status.HTTP_409_CONFLICT)

    return Response("successs")


@api_view(['POST'])
def login(request):
    if not request.headers["Authorization"] == API_KEY:
        return Response("NOT AUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)

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
    if not request.headers["Authorization"] == API_KEY:
        return Response("NOT AUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)
    data = request.data

    if data['password'] != data['password_confirm']:
        raise exceptions.APIException('Passwords do not match!')

    reset_password = Reset.objects.filter(token=data['token']).first()
    if not reset_password:
        # raise exceptions.APIException("Invalid link!")
        return Response("Invalid reset link")

    user = User.objects.filter(email=reset_password.email).first()

    if not user:
        return Response("This user doesn't exist")

    user.set_password(data['password'])
    user.save()

    return Response('success')


def create_qouta(email, type):
    user_email = email
    print("CHECK", email, type)
    # GET USER QOUTA
    try:
        user_exists = UserQouta.objects.filter(user=user_email)
        if user_exists:
            print(user_exists, "User already exists")
            return Response("User already exists")
        else:
            raise exceptions
    except:
        print("Running exception")
        user_account_status = User.objects.get(email=user_3mail)
        status = user_account_status.status
        print(user_account_status)
        if type == subscriptionTypes["trial"]:
            # COMPLETE USER QUOTA FOR PAID WILL BE REDESIGNED
            user_qouta = UserQouta.objects.create(user=user_email, qouta=5)
        elif type == subscriptionTypes["Pro"]:
            # COMPLETE USER QUOTA FOR TRIAL IS NOW $5.25
            user_qouta = UserQouta.objects.create(user=user_email, qouta=20)
        elif type == subscriptionTypes["Business"]:
            # COMPLETE USER QUOTA FOR TRIAL IS NOW $5.25
            user_qouta = UserQouta.objects.create(user=user_email, qouta=50)
        elif type == subscriptionTypes["Enterprise"]:
            # COMPLETE USER QUOTA FOR TRIAL IS NOW $5.25
            user_qouta = UserQouta.objects.create(user=user_email, qouta=80)

    return Response("QOUTA CREATED")

# QOUTA LOGIB


@api_view(['GET'])
def get_user_qouta(request, user_email):
    if not request.headers["Authorization"] == API_KEY:
        return Response("NOT AUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)

    user = user_email
    user_qouta = UserQouta.objects.get(user=user)

    # UserQouta.objects.get(user=user_email)
    user_account = User.objects.get(email=user_email)

    date_joined = user_account.date_joined
    today = datetime.now(timezone.utc)

    time_difference = date_joined - today

    if user_account.status == "Not Activated":

        # SINCE USER WILL ONLY GET THEIR QOUTA WHEN THEY ACTIVATE THEIR ACCOUNT
        # THIS IS SUFFICIENT AS A HANDLER
        return Response("Not Activated", status=status.HTTP_423_LOCKED)

    elif user_account.status == "Trial" and time_difference.days <= -8:
        user_account.status = "Trial Ended"
        user_qouta.qouta = 0
        user_qouta.status = "Trial Ended"
        user_account.save()
        user_qouta.save()
        qouta_serializer = UserQouta.objects.filter(user=user_email)
        serializer = QoutaSerializer(qouta_serializer, many=True)
        return Response(serializer.data)

    # elif user_account.status == "Trial Ended":
    #     user_account.status = "Trial Ended"
    #     user_qouta.qouta = 0
    #     user_qouta.status = "Trial Ended"
    #     user_account.save()
    #     user_qouta.save()
    #     serializer = QoutaSerializer(user_qouta, many=True)
    #     return Response(serializer.data)

    elif user_account.status == "Subscription Expired":
        return Response("Subscription Expired")
    qouta_serializer = UserQouta.objects.filter(user=user_email)
    serializer = QoutaSerializer(qouta_serializer, many=True)
    return Response(serializer.data)


@ api_view(['POST'])
def update_user_qouta(request, user_email):
    user_account = User.objects.get(email=user_email)
    if user_account.status == "Not Activated":

        # SINCE USER WILL ONLY GET THEIR QOUTA WHEN THEY ACTIVATE THEIR ACCOUNT
        # THIS IS SUFFICIENT AS A HANDLER
        return Response("Not Activated", status=status.HTTP_423_LOCKED)
    elif user_account.status == "Trial Ended":
        return Response("Trial Ended", status=status.HTTP_402_PAYMENT_REQUIRED)

    user = user_email
    user = UserQouta.objects.get(user=user)
    date_updated = user.date_updated
    now = datetime.now(timezone.utc)
    seconds_since_midnight = now - date_updated

    main_user_obj = User.objects.get(email=user_email)

    user_account_status = user.status
    # print(seconds_since_midnight.days, "updating!!")
    if(seconds_since_midnight.days >= 1):
        if (main_user_obj.status == "Paid"):
            # WE EVENTUALLY WANT TO ASK USERS IF THEY WANT US TO REGULATE THEIR TRIAL OR NOT
            # ELSE LET THEM USE UNTIL IT IS FINISHED

            # user.qouta = 10
            user.status = "Paid"
            user.date_updated = now
        elif (main_user_obj.status == "Trial"):
            # WE EVENTUALLY WANT TO ASK USERS IF THEY WANT US TO REGULATE THEIR TRIAL OR NOT
            # ELSE LET THEM USE UNTIL IT IS FINISHED

            # user.qouta = 3
            # user.status = "Trail"
            # user.date_updated = now

            pass
        else:
            user.status = "Not Activated"
        user.save()
        print("DAYS LEFT", seconds_since_midnight.days)
    else:
        print("NOT EQUAL", seconds_since_midnight.days)
    return Response("UPDATED!")


@ api_view(['POST'])
def reduce_qouta(request, user_email):
    if not request.headers["Authorization"] == API_KEY:
        return Response("NOT AUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)

    user = user_email
    user = UserQouta.objects.get(user=user_email)
    user.qouta -= 1
    user.save()
    return Response("Reduced!")


@ api_view(['POST'])
def confirm_email(request):
    if not request.headers["Authorization"] == API_KEY:
        return Response("NOT AUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)

    user_email = request.data['email']
    print("EMAIL", user_email)

    # TODO: RUN THIS ONLY IF USER ACCOUNT STATUS IS NOT ACTIVATED
    try:
        check_user = User.objects.get(email=user_email)
        if not check_user.status == "Not Activated":
            return Response("Email Already Confirmed", status=status.HTTP_200_OK)

        check_user.status = "Trial"
        check_user.save()

        user_exists = UserQouta.objects.filter(user=user_email)
        try:
            # //THIS WILL FAIL IF IT ALREADY EXISTS AS UNIQUE IS SET TO TRUE
            create_qouta(user_email, subscriptionTypes["trial"])
        except Exception as E:
            print("NO QOUTA CREATOR", E)

    except Exception as E:
        print("ERROR", E)
        return Response("User with that email doesn't exist!", status=status.HTTP_404_NOT_FOUND)

    return Response("Success")


@api_view(['POST'])
def forgot_password(request):
    if not request.headers["Authorization"] == API_KEY:
        return Response("NOT AUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)
    email = request.data['email']
    token = str(secrets.token_hex(10))
    Reset.objects.create(email=email, token=token)

    url = 'https://uprosal.com/resetpasswordconfirm/'+token

    send_mail("Password Reset", url, settings.EMAIL_HOST_USER, [
              email], fail_silently=False)

    return Response("Success")
