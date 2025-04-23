from rest_framework import serializers
from .models import AnnotationItem, Project

class AnnotationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnotationItem
        fields = ['id', 'text', 'label', 'created_at', 'project']

class ProjectSerializer(serializers.ModelSerializer):
    items = AnnotationItemSerializer(many=True, read_only=True)
    item_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'items', 'item_count']
        read_only_fields = ['created_at']
    
    def get_item_count(self, obj):
        return obj.items.count()
    
    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Project name must be at least 3 characters long")
        return value.strip()
    
    def validate_description(self, value):
        if value and len(value.strip()) < 10:
            raise serializers.ValidationError("Description must be at least 10 characters long")
        return value.strip() if value else value