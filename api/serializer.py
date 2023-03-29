from rest_framework import serializers
from .models import Projects, CoverLetter


class CoverLetterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoverLetter
        fields = ['user', 'letter']


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = ['id','user', 'title', 'description', 'url']
