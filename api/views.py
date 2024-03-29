from django.shortcuts import render
from .models import CoverLetter, Projects, Skills, ContactUs
from .serializer import CoverLetterSerializer, ProjectSerializer, SkillsSerializer
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework import exceptions, status
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.

API_KEY = settings.APIKEY


@api_view(['GET'])
def get_cover_letter(request, email):
    cover_letter = CoverLetter.objects.filter(user=email)
    serializer = CoverLetterSerializer(cover_letter, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_projects(request, email):
    projects = Projects.objects.filter(user=email)
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def update_project(request):
    id = request.data['id']
    project = Projects.objects.get(id=id)
    project.title = request.data["title"]
    project.description = request.data["description"]
    project.url = request.data["url"]
    project.save()
    return Response("success")


@api_view(['POST'])
def save_cover_letter(request):
    serializer = CoverLetterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response("Something Went wrong!", status=status.HTTP_400_BAD_REQUEST)
    return Response("success")


@api_view(['POST'])
def save_projects(request):
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response("success")


@api_view(['POST'])
def delete_projects(request):
    project = Projects.objects.get(id=request.data['id'])
    project.delete()
    return Response("success")


@api_view(['POST'])
def save_skills(request):
    serializer = SkillsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response("success")


@api_view(['GET'])
def get_skills(request, email):
    projects = Skills.objects.filter(user=email)
    serializer = SkillsSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def update_skills(request):
    id = request.data['id']
    skill = Skills.objects.get(id=id)
    skill.skill = request.data["skills"]
    skill.save()
    return Response("success")


@api_view(['POST'])
def contactUs(request):

    data = request.data
    name = data["name"]
    email = data["email"]
    message = data["message"]

    send_mail(f"UprosaL Support From: {email}", message, settings.EMAIL_HOST_USER, [
        "kolosafo@gmail.com"], fail_silently=True)

    ContactUs.objects.create(name=name, message=message)
    return JsonResponse("Success", safe=False, status=200)
