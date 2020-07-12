import os
import sys

SFILE = __file__
SPATH1 = os.path.normpath(os.path.dirname(SFILE))


# Django settings for gradlist project.
SPATH = os.path.realpath(os.path.dirname(__file__))
DEBUG  =  True
TEMPLATE_DEBUG = DEBUG


ADMINS = (
     ('mathew', 'adysys@yahoo.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        # 'NAME': 'C:/Users/CCL/Downloads/icydb.db' ,
        'NAME': '/home/examorigin/myproject/eo.db',                   # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        # 'CONN_MAX_AGE': 60 * 10,  # 10 minutes
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'schapp',                      # Or path to database file if using sqlite3.
#         'USER': 'root',                      # Not used with sqlite3.
#         'PASSWORD': 'chidemavian',                  # Not used with sqlite3.
#         'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#         'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#     }
# }


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.

TIME_ZONE = 'Africa/Lagos'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(SPATH, 'static/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
SITE_URL = 'http://127.0.0.1:8000/'
MEDIA_URL = 'http://127.0.0.1:8000/static/'
LOGIN_REDIRECT_URL ='/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'k9hen(791sx)w6e&l-@j8l@vw)+8jhul9ypqu74#f+#e=nr_wn'

# List of callables that know how to import templates from various sources.

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#         }
#     },
# }


# DEBUG_TOOLBAR_PANELS = {
#     debug_toolbar.panels.profiling.ProfilingPanel

# }

# DEBUG_TOOLBAR_CONFIG = {
#   "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
# }

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    #'django.template.loaders.filesystem.load_template_source',
    #'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.app_directories.Loader',
  #   'django.template.loaders.eggs.load_template_source',
)


# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [os.path.join(BASE_DIR, 'foo', 'bar'), ],
#         'OPTIONS': {
#             # ...
#             'loaders': [
#                 ('django.template.loaders.cached.Loader', [
#                     'django.template.loaders.filesystem.Loader',
#                     'django.template.loaders.app_directories.Loader',
#                 ]),
#             ],
#         },
#     },
# ]



MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'myproject.middleware.ProfileMiddleware',
    # 'silk.middleware.silkymiddleware'
    # 'debug_toolbar.middleware.DebugToolbarMiddleware', #for DDT profiling

    #'pagination.middleware.PaginationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    #'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    )

ROOT_URLCONF = 'myproject.urls'
TPATH = os.path.join(SPATH, 'templates')
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    TPATH
)


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    # 'debug_toolbar',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'django.contrib.sites',
    'myproject.setup',
    'myproject.academics',
    'myproject.student',
    'myproject.sysadmin',
    'myproject.bill',
    'myproject.assessment',
    'myproject.utilities',
    'myproject.lesson',
    'myproject.CBT',
    'myproject.authen',
    #'pagination',
    'south',
    'assignment',
    'transport',
    # 'silk',
)
SESSION_COOKIE_AGE = 1500  #25min
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.yahoomail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'soundfoundation@yahoo.com'
EMAIL_HOST_PASSWORD = 'yuo'
# INTERNAL_IPS = ['127.0.0.1']

