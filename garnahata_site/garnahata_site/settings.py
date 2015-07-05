"""
Django settings for garnahata_site project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'PLEASEREPLACEMEREPLACEMEREPLACEMDONTLEAVEMELIKETHAT'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pipeline',
    'django_jinja',
    'django_jinja.contrib._humanize',
    'django_jinja.contrib._easy_thumbnails',
    'leaflet',

    'compressor',
    'taggit',
    'modelcluster',

    'wagtail.wagtailcore',
    'wagtail.wagtailadmin',
    'wagtail.wagtaildocs',
    'wagtail.wagtailsnippets',
    'wagtail.wagtailusers',
    'wagtail.wagtailimages',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsearch',
    'wagtail.wagtailredirects',
    'wagtail.wagtailforms',

    'catalog',
    'cms_pages',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
)

ROOT_URLCONF = 'garnahata_site.urls'

WSGI_APPLICATION = 'garnahata_site.wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "cms_pages.context_processors.menu_processor"
)

# We don't need a database yet!
DATABASES = {
    'default': {
        # Strictly PostgreSQL
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
    }
}

# Setup Elasticsearch default connection
ELASTICSEARCH_CONNECTIONS = {
    'default': {
        'hosts': 'localhost',
        'timeout': 20
    }
}

LANGUAGE_CODE = 'uk-ua'
TIME_ZONE = 'Europe/Kiev'

USE_I18N = True
USE_L10N = False
USE_TZ = True


TEMPLATE_LOADERS = (
    'django_jinja.loaders.AppLoader',
    'django_jinja.loaders.FileSystemLoader',
)
DEFAULT_JINJA2_TEMPLATE_EXTENSION = '.jinja'
JINJA2_EXTENSIONS = [
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
    "pipeline.jinja2.ext.PipelineExtension"
]


STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
    'pipeline.finders.PipelineFinder',
)

PIPELINE_CSS = {
    'css_all': {
        'source_filenames': (
            'css/bootstrap.css',
            'css/animate.css',
            'css/nav.css',
            'css/header.css',
            'css/news.css',
            'css/style.css',
            'css/responsive.css',
        ),
        'output_filename': 'css/merged.css',
        'extra_context': {},
    },
}

PIPELINE_JS = {
    'js_all': {
        'source_filenames': (
            'js/jquery.js',
            'js/bootstrap.js',
            'js/masonry.pkgd.js',
            'js/jquery.easing.min.js',
            'js/jquery.fittext.js',
            'js/garnahata.js',
        ),
        'output_filename': 'js/merged.js',
    }
}

THUMBNAIL_ALIASES = {
    '': {
        'homepage_news': {'size': (782, 394), 'crop': True},
        'news_thumbnail': {'size': (243, 450), 'crop': False}
    },
}


LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (50.387507803003146, 30.454101562499996),
    'DEFAULT_ZOOM': 12,
}


PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.uglifyjs.UglifyJSCompressor'

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = '/media/'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Application settings
CATALOG_PER_PAGE = 30

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

LOGIN_URL = "/admin/login/"
WAGTAIL_SITE_NAME = 'GarnaHata!'

try:
    from .local_settings import *
except ImportError:
    pass


# Init Elasticsearch connections
from elasticsearch_dsl import connections
connections.connections.configure(**ELASTICSEARCH_CONNECTIONS)
