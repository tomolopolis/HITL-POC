from django.contrib import admin
from django.http import HttpResponse
import csv
from datetime import datetime
from .models import Project, AnnotationItem


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    actions = ['download_annotations']

    def download_annotations(self, request, queryset):
        if len(queryset) > 1:
            self.message_user(request, "Please select only one project to download annotations.")
            return

        project = queryset.first()
        response = HttpResponse(content_type='text/csv')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        response['Content-Disposition'] = f'attachment; filename="{project.name}_labeled_annotations_{timestamp}.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Text', 'Label', 'Created At'])

        # Only include items that have a label
        for item in project.items.exclude(label__isnull=True).exclude(label='').order_by('created_at'):
            writer.writerow([
                item.id,
                item.text,
                item.label,
                item.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])

        return response
    download_annotations.short_description = "Download labeled annotations as CSV"


@admin.register(AnnotationItem)
class AnnotationItemAdmin(admin.ModelAdmin):
    list_display = ('project', 'text', 'label', 'created_at')
    list_filter = ('project', 'label', 'created_at')
    search_fields = ('text', 'label')
    ordering = ('-created_at',)
    raw_id_fields = ('project',) 