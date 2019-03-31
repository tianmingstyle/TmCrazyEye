__author__ = 'tianming'

class ArgvHandle():
    def __init__(self, sys_argvs):
        self.sys_argvs = sys_argvs

    def help_msg(self, err_msg=''):
        """
            打印帮助信息
        """
        msg = """
            %s
            run 交互程序
        """%err_msg
        #print(msg)
        exit(msg)

    def call(self):
        """
            根据用户给的参数调用对应的功能
            python crazyeye_manager.py run
        """
        if len(self.sys_argvs) == 1:
            self.help_msg()

        if hasattr(self, self.sys_argvs[1]):
            func = getattr(self, self.sys_argvs[1])
            func()
        else:
            self.help_msg("no run method")

    def run(self):
        """
            启动用户交互程序
        """
        from backend import ssh_interactive
        ssh_interactive_obj = ssh_interactive.SshHandle(self)
        ssh_interactive_obj.interactive()
