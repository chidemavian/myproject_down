import os, sys  
sys.path.append('C:/windows/www/icy/myproject/')
sys.path.append('C:/windows/www/icy')
os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'  
import django.core.handlers.wsgi  
application = django.core.handlers.wsgi.WSGIHandler()  
