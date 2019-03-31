from django.db import models

# Create your models here.

class Host(models.Model):
    """
        存储主机列表
    """
    name = models.CharField(max_length=32)
    ip = models.GenericIPAddressField(unique=True)
    port = models.SmallIntegerField(default=22)
    idc = models.ForeignKey("IDC",on_delete=models.CASCADE)

    def __str__(self):
        return self.ip

class RemoteUser(models.Model):
    """
        主机用户表
    """
    login_type_choices = [(1,"ssh-key"),(0,"ssh-password")]
    login_type = models.SmallIntegerField(choices=login_type_choices, default=0)
    username = models.CharField(max_length=32)
    pwd = models.CharField(max_length=64)

    class Meta:
        unique_together=(("login_type","username","pwd"),)

    def __str__(self):
        return "{}:{}".format(self.username,self.pwd)


class Host2RemoteUser(models.Model):
    """
        绑定主机和远程主机的对应关系
    """
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    remote_user = models.ForeignKey(RemoteUser,on_delete=models.CASCADE)

    class Meta:
        unique_together=(("host", "remote_user"),)

    def __str__(self):
        return "%s:%s"%(self.host, self.remote_user)

class UserProfile(models.Model):
    """
        堡垒机账号列表
    """
    username = models.CharField(max_length=32, unique=True)
    pwd = models.CharField(max_length=64)
    hostgroup = models.ManyToManyField("HostGroup", null=True, blank=True)
    host_to_remote_user = models.ManyToManyField("Host2RemoteUser", null=True, blank=True)

    def __str__(self):
        return self.username

class HostGroup(models.Model):
    """
        主机组
    """
    name = models.CharField(max_length=32, unique=True)
    host_to_remote_user = models.ManyToManyField("Host2RemoteUser", null=True, blank=True)

    def __str__(self):
        return self.name

class IDC(models.Model):
    """
        IDC机房信息
    """
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name

class AuditLog(models.Model):
    """"
        存储审计日志
    """
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    host_to_remote_user = models.ForeignKey(Host2RemoteUser,on_delete=models.CASCADE)
    login_type_choice = [(0, 'login'), (1, 'cmd'), (2, 'logout')]
    login_type = models.SmallIntegerField(choices=login_type_choice)
    content = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s"%(self.host_to_remote_user, self.content)


class Task(models.Model):
    """
        存储从前端返回过来的任务信息
    """
    task_type_choices = [(0, "cmd"),(1, "file_transfer")]
    task_type = models.SmallIntegerField(choices=task_type_choices)
    user = models.ForeignKey("UserProfile",on_delete=models.CASCADE)
    content = models.CharField(max_length=128)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s"%(self.user, self.content)


class TaskDetail(models.Model):
    """
         存储大任务的结果信息
    """
    task = models.ForeignKey(Task,on_delete=models.CASCADE)
    host_to_remote_user = models.ForeignKey(Host2RemoteUser,on_delete=models.CASCADE)
    result = models.TextField(max_length=256, blank=True, null=True)
    task_status_choices = [(0, "initialized"),(1,"success"),(2,"failed"),(3,"timeout")]
    task_status = models.SmallIntegerField(choices=task_status_choices, default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.host_to_remote_user, self.result)

