import sys, os
import time
import paramiko
from concurrent.futures import ThreadPoolExecutor

def ssh_cmd(sub_task_obj):
     host_to_remote_user = sub_task_obj.host_to_remote_user
     try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host_to_remote_user.host.ip,
                           host_to_remote_user.host.port,
                           host_to_remote_user.remote_user.username,
                           host_to_remote_user.remote_user.pwd,
                           timeout=5)
        stdin, stdout, stderr = ssh_client.exec_command(sub_task_obj.task.content)
        print('-----------------stdout&stderr-----------------------------------')
        stdout_res = stdout.read().decode('utf-8')
        stderr_res = stderr.read().decode('utf-8')
        print("stdout_res:",stdout_res)
        print("stderr_res:",stderr_res)
        #sub_task_obj = models.TaskDetail.objects.get(task=task_obj, host_to_remote_user=host_to_remote_user)
        sub_task_obj.result=stderr_res+stdout_res
        if stderr_res:
            sub_task_obj.task_status=2
        else:
            sub_task_obj.task_status=1


     except Exception as e:
         sub_task_obj.result= str(e)
         sub_task_obj.task_status=2
         print(e)
     sub_task_obj.save()

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(base_dir)
    sys.path.append(base_dir)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TmCrazyEye.settings')
    import django
    django.setup()
    from app01 import models

    if len(sys.argv) == 1:
         exit("task_id is not provided!")
    task_id = sys.argv[1]
    task_obj = models.Task.objects.get(id=task_id)

    pool = ThreadPoolExecutor(5)
    for sub_task_obj in task_obj.taskdetail_set.all():
        pool.submit(ssh_cmd, sub_task_obj)
    #ssh_cmd(task_obj)
    #task_obj.content = "task test"
    #time.sleep(8)
    #task_obj.save()
