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

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_ROOT = os.path.join(BASE_DIR, "static")

PDFS_STORAGE = os.path.join(STATIC_ROOT, 'files')

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
    'django.contrib.sitemaps',
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
    'tinymce',

    'catalog',
    'cms_pages',
    'fs',
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

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND':
            'wagtail.wagtailsearch.backends.elasticsearch.ElasticSearch',
        'URLS': ['http://localhost:9200'],
        'INDEX': 'garnahata_cms',
        'TIMEOUT': 5,
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
                "django.core.context_processors.debug",
                "django.core.context_processors.media",
                "django.core.context_processors.static",
                "django.core.context_processors.tz",
                "django.core.context_processors.request",
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
                "pipeline.jinja2.ext.PipelineExtension"
            ]
        }
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "OPTIONS": {
            "context_processors": (
                "django.contrib.auth.context_processors.auth",
                "django.core.context_processors.debug",
                "django.core.context_processors.media",
                "django.core.context_processors.static",
                "django.core.context_processors.tz",
                "django.core.context_processors.request",
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

PIPELINE_CSS = {
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
    },
}

PIPELINE_JS = {
    'js_all': {
        'source_filenames': (
            'js/jquery.js',
            'js/bootstrap.js',
            "js/bootstrap3-typeahead.js",
            'js/imagesloaded.pkgd.js',
            'js/masonry.pkgd.js',
            'js/jquery.easing.min.js',
            'js/jquery.fittext.js',
            'js/social-likes.min.js',
            'js/garnahata.js',
        ),
        'output_filename': 'js/merged.js',
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
        },
        'yandex': {
            'js': 'js/Yandex.js',
            'auto-include': True
        }
    }
}


PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.uglifyjs.UglifyJSCompressor'

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = '/media/'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Application settings
CATALOG_PER_PAGE = 20

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

DATE_FORMAT = "d.m.Y"
LOGIN_URL = "/admin/login/"
WAGTAIL_SITE_NAME = 'GarnaHata!'

try:
    from .local_settings import *
except ImportError:
    pass


# Init Elasticsearch connections
from elasticsearch_dsl import connections
connections.connections.configure(**ELASTICSEARCH_CONNECTIONS)
