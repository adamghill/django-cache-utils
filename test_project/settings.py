import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(PROJECT_ROOT))

SECRET_KEY = '9k!n(bx!_yovt7=@&fboic$wj3)(^m_-0+@inp+mowxi45p1!w'

# Required to make sure that cache_utils can be imported
from cache_utils.group_backend import CacheClass

CACHES = {
    'default': {
        'BACKEND': 'cache_utils.group_backend.CacheClass',
        'LOCATION': '127.0.0.1:11211',
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = (
    'cache_utils',
)
