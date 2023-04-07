from django.shortcuts import render
from .models import CoverLetter, Projects, Skills
from .serializer import CoverLetterSerializer, ProjectSerializer, SkillsSerializer
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework import exceptions, status
from django.conf import settings

# Create your views here.

API_KEY = settings.APIKEY


@api_view(['GET'])
def get_cover_letter(request, email):

    if not request.headers["Authorization"] == API_KEY:
        return Response("NOT AUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)
    cover_letter = CoverLetter.objects.filter(user=email)
    serializer = CoverLetterSerializer(cover_letter, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_projects(request, email):

    if not request.headers["Authorization"] == API_KEY:
        return Response("NOT AUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)
    projects = Projects.objects.filter(user=email)
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def update_project(request):

    if not request.headers["Authorization"] == API_KEY:
        return Response("NOT AUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)
    id = request.data['id']
    project = Projects.objects.get(id=id)
    project.title = request.data["title"]
    project.description = request.data["description"]
    project.url = request.data["url"]
    project.save()
    return Response("success")


@api_view(['POST'])
def save_cover_letter(request):
    if not request.headers["Authorization"] == API_KEY:
        return Response("NOT AUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)
    serializer = CoverLetterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response("Something Went wrong!", status=status.HTTP_400_BAD_REQUEST)
    return Response("success")


@api_view(['POST'])
def save_projects(request):

    if not request.headers["Authorization"] == API_KEY:
        return Response("NOT AUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)
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

    if not request.headers["Authorization"] == API_KEY:
        return Response("NOT AUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)
    serializer = SkillsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response("success")


@api_view(['GET'])
def get_skills(request, email):

    if not request.headers["Authorization"] == API_KEY:
        return Response("NOT AUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)
    projects = Skills.objects.filter(user=email)
    serializer = SkillsSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def update_skills(request):

    if not request.headers["Authorization"] == API_KEY:
        return Response("NOT AUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)
    id = request.data['id']
    skill = Skills.objects.get(id=id)
    skill.skill = request.data["skills"]
    skill.save()
    return Response("success")
