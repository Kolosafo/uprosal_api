from rest_framework import serializers
from .models import Projects, CoverLetter, Skills


class CoverLetterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoverLetter
        fields = ['user', 'job_description', 'cover_letter']


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = ['id', 'user', 'title', 'description', 'url']


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = ['id', 'user', 'skill']
