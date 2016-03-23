import os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
STATICFILES_DIRS = os.path.join(SITE_ROOT, 'static/')

DEFAULT_SAVE_DIR=os.path.join(STATICFILES_DIRS, "output")

#PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))