from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import AnnotationItem, Project
from .serializers import AnnotationItemSerializer, ProjectSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        queryset = Project.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(name__icontains=search) | queryset.filter(description__icontains=search)
        return queryset.order_by('-created_at')
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.items.exists():
            return Response(
                {"error": "Cannot delete project with existing annotation items. Please delete the items first."},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        project = self.get_object()
        return Response({
            'total_items': project.items.count(),
            'labeled_items': project.items.exclude(label__isnull=True).count(),
            'unlabeled_items': project.items.filter(label__isnull=True).count(),
        })
    
    @action(detail=True, methods=['get'])
    def completed_annotations(self, request, pk=None):
        project = self.get_object()
        completed_items = project.items.exclude(label__isnull=True).order_by('-created_at')
        serializer = AnnotationItemSerializer(completed_items, many=True)
        return Response(serializer.data)

class AnnotationItemViewSet(viewsets.ModelViewSet):
    queryset = AnnotationItem.objects.all()
    serializer_class = AnnotationItemSerializer
    
    def get_queryset(self):
        queryset = AnnotationItem.objects.all()
        project_id = self.request.query_params.get('project', None)
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset