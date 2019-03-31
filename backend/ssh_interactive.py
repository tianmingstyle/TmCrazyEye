__author__ = 'tianming'
from app01 import models
from backend import paramiko_ssh
from app01 import models

class SshHandle():
    def __init__(self, argvhandle_instance):
        self.argvhandle_instance = argvhandle_instance
        self.models = models

    def validateUser(self):
        count = 0
        while count < 3:
            username=input("input your username,please:").strip()
            passwd=input("input your passwd,please:").strip()

            if models.UserProfile.objects.filter(username=username).exists():

                userobj = models.UserProfile.objects.filter(username=username).first()
                self.username = userobj
                print(userobj.pwd)
                if passwd == userobj.pwd:
                    return True
                else:
                    count += 1
            else:
                count += 1

    def interactive(self):
        """
            现在开始验证堡垒机账号和密码，并列出该账号下的主机和主机组列表
        """
        if self.validateUser():
            print("Welcome to CrazyEye system! The following host or hostgroup you can login")
            #列出主机组

            while True:
                host_group_list = models.HostGroup.objects.all()
                #ungrouped_host_list = models.UserProfile.objects.filter(username=self.username).host_to_remote_user.all()
                for index,host_group_obj in enumerate(host_group_list):
                    print("%s\t[%s]%s"%(index,host_group_obj, host_group_obj.host_to_remote_user.count()))
                print("z ungroup_host[%s]"%models.UserProfile.objects.filter(username=self.username).first().host_to_remote_user.count())

                #选择主机组
                group_choice = input(">>>please select hostgroup:").strip()
                if group_choice.isdigit():
                    choice_group = host_group_list[int(group_choice)]
                elif group_choice == 'z':
                    choice_group = models.UserProfile.objects.filter(username=self.username).first()
                else:
                    continue
                #列出该组下的所有主机和用户
                while True:
                    for index, htru in enumerate(choice_group.host_to_remote_user.all()):
                        print("%s\t[%s]"%(index,htru))
                    #选择某一台主机并开始登入

                    host_choice = input(">>>please select host:").strip()
                    if host_choice.isdigit():
                        hostobj= choice_group.host_to_remote_user.all()[int(host_choice)]
                        #print(hostobj.host.ip)
                        #print(hostobj.host.port)
                        #print(hostobj.remote_user.username)
                        #print(hostobj.remote_user.pwd)
                        #将所选的主机ip，port,user,pwd，传给paramiko来进行远程连接
                        #打印一下所选的主机ip，port,user,pwd
                        print("Wait...loinging to %s"%hostobj.host)
                        print('--------------info start---------------------')
                        print("host: %s, port: %s, user: %s, pwd: %s"%(hostobj.host.ip,
                                                                       hostobj.host.port,
                                                                       hostobj.remote_user.username,
                                                                       hostobj.remote_user.pwd))
                        print('--------------info end-----------------------')
                        # ready to connect!
                        #paramiko_ssh.ssh_connect(self,
                        #                         hostobj.host.ip,
                        #                         hostobj.host.port,
                        #                         hostobj.remote_user.username,
                        #                         hostobj.remote_user.pwd)
                        paramiko_ssh.ssh_connect(self,hostobj)
                    if host_choice == "b":
                        break


        else:
            print("you have no rights to login this system.")
