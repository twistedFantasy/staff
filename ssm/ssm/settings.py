"""
Django settings for ssm project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import datetime

NAME = 'SSM'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/hSIMPLE_JWTowto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nda)q)yyg@fse_ugenqof9h0^_atj)6+xc&lm@v7yi+1gbmplk'

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ['ENV'] in ['dev', 'stg']:
    DEBUG = True
    ALLOWED_HOSTS = ['*']
else:
    DEBUG = False
    ALLOWED_HOSTS = ['codex-soft']
ENV = os.environ['ENV']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'taggit',
    'reversion',
    'corsheaders',
    'djcelery_email',
    'debug_toolbar',
    'rest_framework',
    'django_filters',
    'health_check',     # required
    'health_check.db',  # stock Django health checkers

    # ssm
    'ssm.core.apps.Config',
    'ssm.core',
    'ssm.events',
    'ssm.projects',
    'ssm.skills',
    'ssm.users',
    'ssm.absences',
    'ssm.assessments',
    'ssm.reports',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # must come after auth above
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ssm.urls'
AUTH_USER_MODEL = 'users.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ssm.wsgi.application'


# database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USER'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'HOST': os.environ['DATABASE_HOST'],
        'PORT': os.environ['DATABASE_PORT'],
        'TEST': {
            'NAME': os.environ['TEST_DATABASE_NAME'],   # name to use for testrunner db
            'CHARSET': 'utf8',
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")  # for pretty django admin in release mode
STATICFILES_DIRS = [
    '/var/staff/ssm/external_static/',
]

# email
EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = 'do.not.reply@codex-soft.com'

# redis / celery
CELERY_DATE_FORMAT = '%Y-%m-%d %H:%M:%S %z'
CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']
BROKER_TRANSPORT_OPTIONS = {'socket_timeout': 300}  # 5 minutes
CELERY_RESULT_BACKEND = os.environ['CELERY_RESULT_BACKEND']
CELERY_TASK_RESULT_EXPIRES = 3600  # 1 hour
CELERY_TASK_DEFAULT_EXCHANGE_TYPE = "direct"
CELERY_TASK_DEFAULT_ROUTING_KEY = "celery"
CELERY_TASK_DEFAULT_EXCHANGE = "celery"
CELERY_TASK_DEFAULT_QUEUE = "celery-general"
CELERY_TASK_QUEUES = {
    "celery-general": {
        "exchange": "celery",
        "exchange_type": "topic",
        "binding_key": "general.#",
    },
    "celery-report": {
        "exchange": "report",
        "exchange_type": "topic",
        "binding_key": "report.#",
    }
}
CELERY_TASK_ROUTES = {
    "ssm.users.tasks.example.ExampleTask": {
        "queue": "celery-general",
        "routing_key": "general.example",
    },
    "ssm.reports.tasks.working_hours.WorkingHours": {
        "queue": "celery-report",
        "routing_key": "report.working_hours",
    }
}
CELERY_IMPORTS = [
    "ssm.users.tasks.example",
    "ssm.reports.tasks.working_hours",
]

# auth
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(seconds=1209600),  # 2 weeks
    'AUTH_HEADER_TYPES': ('Bearer', 'JWT'),
}

# cors
CORS_ORIGIN_ALLOW_ALL = bool(os.environ['CORS_ORIGIN_ALLOW_ALL'])

# rest framework
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '10000/day'
    },
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.OrderingFilter',
    ],
    'URL_FORMAT_OVERRIDE': 'response_format',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}

# debug toolbar
def show_toolbar(request):
    try:
        return not request.is_ajax() and request.user.has_tag('toolbar')
    except:
        return False
#
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'ssm.settings.show_toolbar',
    'PROFILER_MAX_DEPTH': 25,
}
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    # 'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

# notifications
BIRTHDAY_SUBJECT = "Happy Birthday!"
BIRTHDAY_MESSAGE = "Hey! Happy Birthday from Codex-Soft, be the best!"
ASSESSMENT_SUBJECT = "Assessment reminder"
ASSESSMENT_MESSAGE = "Hey, just a friendly reminder, assessment is today. Are you ready?"

MEDIA_ROOT = '/var/ssm/data/'
MEDIA_URL = '/media/'

# admin
ADMIN_URL = os.environ['ADMIN_URL']

# Codemirror
CODEMIRROR_PATH = 'components/codemirror-5.48.2'  # latest changeset from github

# tests
TEST_STAFFUSER_EMAIL = 'test.staffuser@gmail.com'
TEST_STAFFUSER_PASSWORD = 'test.staffuser.password'
TEST_SIMPLEUSER_EMAIL = 'test.simpleuser@gmail.com'
TEST_SIMPLEUSER_PASSWORD = 'test.simpleuser.password'
