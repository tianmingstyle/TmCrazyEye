import json
from app01 import models
import subprocess
from django import conf

class MultiTaskManager:
    def __init__(self, request):
        self.request = request
        self.run_task()

    def task_parse(self):
        """
            解析任务
        """
        #print(type(self.request.POST.get("task_data")))
        self.task_data = json.loads(self.request.POST.get("task_data"))
        task_type = self.task_data.get("task_type")
        #下面已反射的方式判断任务的类型是执行命令还是文件传输，然后执行相应的类方法
        if hasattr(self, task_type):
            func = getattr(self, task_type)
            func()
        else:
            print("can not find task.", task_type)

    def run_task(self):

        self.task_parse()

    def cmd(self):
        """
            run batch command method
            1.将从前端返回的信息存储到数据库里
            2.触发批量任务,并且不阻塞
            3.返回任务的ID给前端
        """
        print("ready to run batch cmd...")
        user_obj = models.UserProfile.objects.get(username=self.request.session["username"])

        print(self.task_data.get("cmd"))
        task_obj = models.Task.objects.create(
            task_type=0,
            user=user_obj,
            content=self.task_data.get("cmd")
        )
        print("task job id is :",task_obj.id)

        task_log_list = []
        selected_host_ids = set(self.task_data.get("selected_host"))

        for host_id in selected_host_ids:
            task_log_list.append(
                models.TaskDetail(   #这里不需要objects.create
                    task=task_obj,
                    host_to_remote_user_id=host_id
                )
            )

        models.TaskDetail.objects.bulk_create(task_log_list)
        #将任务ID返回给前端
        self.task_id = task_obj.id
        #不阻塞的方式触发任务执行
        script_path = "python %s/backend/task_running.py %s"%(conf.settings.BASE_DIR, self.task_id)
        subprocess.Popen(script_path, shell=True)

    def file_transfer(self):
        """
            file transfer method
        """
        pass
