"""
Django settings for garnahata_site project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django_jinja.builtins import DEFAULT_EXTENSIONS

def get_env_str(k, default):
    return os.environ.get(k, default)

def get_env_str_list(k, default=""):
    if os.environ.get(k) is not None:
        return os.environ.get(k).strip().split(" ")
    return default

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

STATIC_URL = '/static/'
MEDIA_ROOT = get_env_str('MEDIA_ROOT', os.path.join(BASE_DIR, "media"))
STATIC_ROOT = get_env_str('STATIC_ROOT', os.path.join(BASE_DIR, "static"))
MEDIA_URL = '/media/'

PDFS_STORAGE = get_env_str('PDFS_STORAGE', os.path.join(STATIC_ROOT, 'files'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_str('SECRET_KEY', 'PLEASEREPLACEMEREPLACEMEREPLACEMDONTLEAVEMELIKETHAT')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = get_env_str_list('ALLOWED_HOSTS', [])


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'pipeline',
    'easy_thumbnails',
    'django_jinja',
    'django_jinja.contrib._humanize',
    'django_jinja.contrib._easy_thumbnails',
    'leaflet',

    'compressor',
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',

    'modelcluster',
    'taggit',
    'tinymce',

    'catalog',
    'cms_pages',
    'fs',
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
)

ROOT_URLCONF = 'garnahata_site.urls'

WSGI_APPLICATION = 'garnahata_site.wsgi.application'


# We don't need a database yet!
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_str('DB_NAME', None),
        'USER': get_env_str('DB_USER', None),
        'PASSWORD': get_env_str('DB_PASS', None),
        'HOST': get_env_str('DB_HOST', None),
        'PORT': get_env_str('DB_PORT', 5432)
    }
}

LANGUAGE_CODE = 'uk-ua'
TIME_ZONE = 'Europe/Kiev'

USE_I18N = True
USE_L10N = False
USE_TZ = True


TEMPLATES = [
    {
        "BACKEND": "django_jinja.backend.Jinja2",
        "APP_DIRS": True,
        "OPTIONS": {
            "match_extension": ".jinja",
            "context_processors": (
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "cms_pages.context_processors.menu_processor",
                "cms_pages.context_processors.expose_settings",
            ),
            "extensions": DEFAULT_EXTENSIONS + [
                "jinja2.ext.do",
                "jinja2.ext.loopcontrols",
                "jinja2.ext.with_",
                "jinja2.ext.i18n",
                "jinja2.ext.autoescape",
                "django_jinja.builtins.extensions.CsrfExtension",
                "django_jinja.builtins.extensions.CacheExtension",
                "django_jinja.builtins.extensions.TimezoneExtension",
                "django_jinja.builtins.extensions.UrlsExtension",
                "django_jinja.builtins.extensions.StaticFilesExtension",
                "django_jinja.builtins.extensions.DjangoFiltersExtension",
                "pipeline.jinja2.PipelineExtension",
            ]
        }
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "OPTIONS": {
            "context_processors": (
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "cms_pages.context_processors.menu_processor",
                "cms_pages.context_processors.expose_settings",
            )
        },
        "APP_DIRS": True
    },
]

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
    'pipeline.finders.PipelineFinder',
)

PIPELINE = {
    'STYLESHEETS': {
        'css_all': {
            'source_filenames': (
                'css/bootstrap.css',
                'css/animate.css',
                'css/nav.css',
                'css/header.css',
                'css/news.css',
                'css/social-likes_flat.css',
                'css/style.css',
                'css/responsive.css',
            ),
            'output_filename': 'css/merged.css',
            'extra_context': {},
        }
    },

    'JAVASCRIPT': {
        'js_all': {
            'source_filenames': (
                'js/jquery.js',
                'js/bootstrap.js',
                "js/bootstrap3-typeahead.js",
                'js/imagesloaded.pkgd.js',
                'js/jquery.easing.min.js',
                'js/jquery.fittext.js',
                'js/social-likes.js',
                'js/garnahata.js',
            ),
            'output_filename': 'js/merged.js',
        }
    }
}

THUMBNAIL_ALIASES = {
    '': {
        'homepage_news': {'size': (782, 394), 'crop': True},
        'news_thumbnail': {'size': (243, 450), 'crop': False},
        'address_thumbnail': {'size': (475, 336), 'crop': True},
        'small_thumbnail': {'size': (64, 64), 'crop': True},
    },
}


LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (50.387507803003146, 30.454101562499996),
    'DEFAULT_ZOOM': 10,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 18,
    'TILES': [],
    'OVERLAYS': [],

    'PLUGINS': {
        'markercluster': {
            'css': ['css/MarkerCluster.Default.css', 'css/MarkerCluster.css'],
            'js': 'js/leaflet.markercluster.js',
            'auto-include': True
        }
    }
}


PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.uglifyjs.UglifyJSCompressor'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Application settings
CATALOG_PER_PAGE = 20

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

DATE_FORMAT = "d.m.Y"
LOGIN_URL = "/admin/login/"
WAGTAIL_SITE_NAME = 'GarnaHata!'

ELASTICSEARCH_DSN = get_env_str('ELASTICSEARCH_DSN', 'localhost:9200')

# Setup Elasticsearch default connection
ELASTICSEARCH_CONNECTIONS = {
    'default': {
        'hosts': ELASTICSEARCH_DSN,
        'timeout': 20
    }
}

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND':
            'wagtail.search.backends.elasticsearch6',
        'URLS': [ ELASTICSEARCH_DSN ],
        'INDEX': 'garnahata_cms',
        'TIMEOUT': 5,
    }
}

GOOGLE_ANALYTICS_ID = get_env_str('GOOGLE_ANALYTICS_ID', None)

try:
    from .local_settings import *
except ImportError:
    pass

# Init Elasticsearch connections
from elasticsearch_dsl import connections
connections.connections.configure(**ELASTICSEARCH_CONNECTIONS)
