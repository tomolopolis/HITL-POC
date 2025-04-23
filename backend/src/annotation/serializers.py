from rest_framework import serializers
from .models import AnnotationItem, Project

class AnnotationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnotationItem
        fields = ['id', 'text', 'label', 'created_at', 'project']

class ProjectSerializer(serializers.ModelSerializer):
    items = AnnotationItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'items']