"""
Django settings for rtarchviz project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import dj_database_url
# import environmental variables set locally
if os.path.exists('env.py'):
    import env

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['rtarchviz.herokuapp.com', 'localhost', '10.11.12.105']

# Use custom User class for accounts
AUTH_USER_MODEL = 'accounts.User'
# Use custom Authentication Backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'accounts.backends.EmailAuth',
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'pages',
    'homepage',
    'accounts',
    'blog',
    'products',
    'cart',
    'checkout',
    # 3rd party apps:
    'bootstrap4',
    'tinymce',
    'disqus',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rtarchviz.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # add context processors for media files
                'django.template.context_processors.media',
                # cart
                'cart.contexts.cart_contents',
                'products.contexts.owned_assets'
            ],
        },
    },
]

WSGI_APPLICATION = 'rtarchviz.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-uk'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


DISQUS_WEBSITE_SHORTNAME = os.environ.get('DISQUS_WEBSITE_SHORTNAME')
DISQUS_API_KEY = os.environ.get('DISQUS_API_KEY')
SITE_ID = 1

TINYMCE_JS_URL = 'https://cdnjs.cloudflare.com/ajax/libs/tinymce/4.7.9/tinymce.min.js'
TINYMCE_DEFAULT_CONFIG = {
    'theme': "modern",
    'language': 'en_GB',
    'plugins': 'advlist, autolink, lists, link, image, charmap, print, preview, hr,     \
                anchor, pagebreak, searchreplace, wordcount, visualblocks, visualchars, \
                code, fullscreen, insertdatetime, media, nonbreaking, save, table,      \
                contextmenu, directionality, emoticons, template, paste, textcolor,     \
                colorpicker, textpattern, imagetools, codesample, toc, autoresize,      \
                autosave',
    'toolbar1': 'undo redo | insert | styleselect | bold italic |   \
                 alignleft aligncenter alignright alignjustify |    \
                 bullist numlist outdent indent | link image',  
    'toolbar2': 'print preview media | forecolor backcolor emoticons | codesample',
    }

# The following causes 'Synchronous SMLHttpRequest warning
# when set to True and the tinyMCE editor stops working
# the compressor is supposed to gzip all js and make the
# tinyMCE editor load faster and result in fewer requests
# Investigate!
TINYMCE_COMPRESSOR = False

# STRIPE Payments settings
STRIPE_PUBLISHABLE = os.environ.get('STRIPE_PUBLISHABLE')
STRIPE_SECRET = os.environ.get('STRIPE_SECRET')

try:
    if os.environ["ENV"] == 'development':
        """
        DEVELOPMENT environment settings
        use for local development
        """
        print "***You are in development mode"

        # Turn on django debug mode
        print "***debug mode is ON"
        DEBUG = True

        # Add debug toolbar
        INSTALLED_APPS.append('debug_toolbar')
        MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
        INTERNAL_IPS = ('127.0.0.1',)
        print "***Debug Toolbar is ON"

        # Static files for local decelopment (CSS, JavaScript, Images)
        STATIC_URL = '/static/'
        STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"), )
        STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
        MEDIA_URL = '/media/'

        if "DATABASE_URL" in os.environ:
            # Use for testing using production db
            print "***Using production PostgreSQL dtabase providion on Heroku for development"
            DATABASES = {
                'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
            }
        else:
            # using the default local sqlite db
            print "***Using Django's local sqlite db for development"
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
                }
        }

    elif os.environ["ENV"] == 'production':
        """
        PRODUCTION environment settings
        """

        DEBUG = False
        # Log DEBUG information to the console
        LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                },
            },
            'loggers': {
                'django': {
                    'handlers': ['console'],
                    'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
                },
            },
        }

        # AWS S3 settings for storing and serving static and media files
        INSTALLED_APPS.append('storages')
        AWS_S3_OBJECT_PARAMETERS = {
            'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
            'CacheControl': 'max-age=94608000',
        }
        AWS_STORAGE_BUCKET_NAME = 'rtarchviz'
        AWS_S3_REGION_NAME = 'eu-west-1'
        AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
        AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
        AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
        STATICFILES_LOCATION = 'static'
        STATICFILES_STORAGE = 'custom_storages.StaticStorage'
        MEDIAFILES_LOCATION = 'media'
        DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
        STATIC_URL = '/static/'

        # Add whitenoise for deploying app with static files to Heroku 
        MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')

        # Use production Postgres database provisioned on Heroku
        if "DATABASE_URL" in os.environ:
            DATABASES = {
            'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
        }
        else:
            print "***no production database found. Provision one in Heroku and link to it using env variable 'DATABASE_URL'"

except KeyError:
    print "***ENV variable not set. Please set the environment variable 'ENV' to 'development' or 'production'"

# Settings for User Password Recovery
if "EMAIL_HOST_USER" and "EMAIL_HOST_PASSWORD" in os.environ:
    # Email setup for sending password recovery emails to users from a gmail account
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com' # need to 'Allow less secure apps' in gmail account settings
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER') # email address
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD') # password
    EMAIL_PORT = 587
else:
    # Print password reset email to the console
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'