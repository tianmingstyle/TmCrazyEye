from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from app01 import models
from backend.multitask import MultiTaskManager
import json
# Create your views here.


def index(request):
    val = request.session.get("isLogin", None)
    if val:
        return render(request, 'index.html')
    return redirect('/login.html')

#@ login_required
#def index(request):
#
#    return render(request, 'index.html')


def login(request):
    error_msg = ''
    if request.method == 'POST':
        username = request.POST.get("username").strip()
        password = request.POST.get("password").strip()
        print("username:%s; password:%s"%(username, password))
        if models.UserProfile.objects.filter(username=username).exists():
            pwd = models.UserProfile.objects.filter(username=username).first()
            if pwd.pwd == password:
                #print(111111111111)
                #request.session['user'] = models.UserProfile.objects.filter(username=username)
                request.session['username']=username
                request.session['isLogin']=True
                request.session['baoleiji']="192.168.2.30"
                print(request.session)
                return redirect('/')
            else:
                error_msg = "密码不正确"
                return render(request, 'login.html', {'error_msg': error_msg})
        else:
            error_msg = '用户名不存在'
            return render(request, 'login.html',{'error_msg': error_msg})
    return render(request, 'login.html',{'error_msg': error_msg})

def logout(request):
    request.session.clear()
    return redirect('/')


def web_ssh(request):
    return render(request, 'web_ssh.html')


def batch_cmd(request):
    group_host_list = models.HostGroup.objects.filter(userprofile__username=request.session['username'])
    print("group_host_list", group_host_list)
    ungroup_host_list = models.Host2RemoteUser.objects.filter(userprofile__username=request.session['username'])
    return render(request, 'batch_cmd.html', {"group_host_list": group_host_list,
                                                "ungroup_host_list": ungroup_host_list
                                              })

def batch_cmd_mgr(request):
    print(request.POST)
    task_data = json.loads(request.POST.get("task_data"))

    #print("task_data", task_data.get("selected_host"))
    selected_hosts = task_data.get("selected_host")
    command = task_data.get("cmd")
    print("selected_host: %s, command:%s"%(selected_hosts,command))
    task_obj = MultiTaskManager(request)
    return HttpResponse(task_obj.task_id)