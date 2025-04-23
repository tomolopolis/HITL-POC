from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnnotationItemViewSet, ProjectViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'items', AnnotationItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]