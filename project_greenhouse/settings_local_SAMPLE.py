from .settings import *

DEBUG = True

SECRET_KEY = ''

ALLOWED_HOSTS += ['0.0.0.0', '127.0.0.1']

VAGRANTAPI_URL = "https://app.vagrantup.com/api/v1/"
VAGRANTAPI_KEY = ""


SHELL_PLUS = "ipython"

LOGGING['handlers']['splunk']['token'] = os.getenv('SPLUNK_TOKEN', '')
LOGGING['handlers']['splunk']['host'] = os.getenv('SPLUNK_HOST', '')
LOGGING['handlers']['splunk']['port'] = int(os.getenv('SPLUNK_PORT', ''))




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'greenhouse',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '5432',
    }
}


MAX_POOL = 8
MEMORY_FREELIMIT = 1024 * 1024 * 512  # 512MB
RUN_MINUTES = 50
SLEEP_SECONDS = 60