import os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
STATICFILES_DIRS = os.path.join(SITE_ROOT, 'static/')

DEFAULT_SAVE_DIR=os.path.join(STATICFILES_DIRS, "output")

#PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'django': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
            'formatter': 'verbose'
        },
        'app': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'app.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['django'],
            'propagate': True,
            'level':'DEBUG',
        },
        'MYAPP': {
            'handlers': ['app'],
            'level': 'DEBUG',
        },
    }
}