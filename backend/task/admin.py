from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'owner')
    search_fields = ('title', 'description', 'owner__username')
    ordering = ('-created_at',)

admin.site.register(Task, TaskAdmin)