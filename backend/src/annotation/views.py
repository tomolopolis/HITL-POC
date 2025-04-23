from rest_framework import viewsets
from .models import AnnotationItem, Project
from .serializers import AnnotationItemSerializer, ProjectSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class AnnotationItemViewSet(viewsets.ModelViewSet):
    queryset = AnnotationItem.objects.all()
    serializer_class = AnnotationItemSerializer
    
    def get_queryset(self):
        queryset = AnnotationItem.objects.all()
        project_id = self.request.query_params.get('project', None)
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset