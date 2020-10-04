# SECURITY WARNING: keep the secret key used in production secret!
from sample_data_generator.settings import BASE_DIR
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dvbrv7@)#6kf7vkd1k9x2ssua7_)+)zbv3e4c1+kf97o*#yvm(@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

