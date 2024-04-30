from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Project)
admin.site.register(ProjectTeam)
admin.site.register(Status)
admin.site.register(ProjectModule)
# admin.site.register(Task)
admin.site.register(UserTask)

@admin.register(Task)
class ProjectTaskAdmin(admin.ModelAdmin):
    list_display = ["id","project","priority","status","task_name","created_at","description","totalMinutes", 'updated_at']


