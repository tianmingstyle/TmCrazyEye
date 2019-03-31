from django.contrib import admin
from . import models
# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    #listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'task_type','user','content')

class TaskDetailAdmin(admin.ModelAdmin):
    #listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'host_to_remote_user','result','task_status', 'date')
admin.site.register(models.Host)
admin.site.register(models.RemoteUser)
admin.site.register(models.Host2RemoteUser)
admin.site.register(models.UserProfile)
admin.site.register(models.HostGroup)
admin.site.register(models.IDC)
admin.site.register(models.AuditLog)
admin.site.register(models.Task,TaskAdmin)
admin.site.register(models.TaskDetail,TaskDetailAdmin)