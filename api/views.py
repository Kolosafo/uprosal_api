from django.shortcuts import render
from .models import CoverLetter, Projects
from .serializer import CoverLetterSerializer, ProjectSerializer
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework import exceptions, status

# Create your views here.


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
