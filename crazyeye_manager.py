import os, sys



if __name__ == '__main__':
    #print(sys.argv)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TmCrazyEye.settings')
    import django
    django.setup()
    from backend import main
    interactive_obj = main.ArgvHandle(sys.argv)
    interactive_obj.call()