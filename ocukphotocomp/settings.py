# Django settings for ocukphotocomp project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Andrew Rowson', 'andrew@growse.com'),
)

CDN_URL = ('cdn1.res.growse.com')

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ocukphotocomp_growse_com_django',                      # Or path to database file if using sqlite3.
        'USER': 'ocukphotocomp_growse_com',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-uk'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/'

#Customer MEDIA URL for ocukphotocomp photos
PHOTO_URL = (
	'http://ocukimages1.growse.com/',
	'http://ocukimages2.growse.com/',
	'http://ocukimages3.growse.com/',
	'http://ocukimages4.growse.com/',
)



# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
STATIC_ROOL='/var/www/growse.com/res/django-static/ocukphotocomp/'
STATICFILES_DIRS=('/home/growse/django-sites/ocukphotocomp/static/',)
STATIC_URL='//cdn1.res.growse.com/django-static/ocukphotocomp/'
STATICFILES_STORAGE='pipeline.storage.PipelineCachedStorage'
PIPELINE_STORAGE = 'pipeline.storage.PipelineFinderStorage'
PIPELINE_CSS = {
    'photocomp': {
        'source_filenames': (
          'css/*.css',
        ),
        'output_filename': 'css/photocomp.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
}
PIPELINE_JS = {
    'stats': {
        'source_filenames': (
          'js/jquery-*.min.js',
          'js/jquery.*.js',
          'js/scripts.js',
        ),
        'output_filename': 'js/photocomp.js',
    }
}
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.cssmin.CssminCompressor'
PIPELINE_JS_COMPRESSOR = None 

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'g%l6i8$k8oc2%ck(i65a=0z7es@a4%oc9h2rrop=v^lmoy2+$y'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'ocukphotocomp.photocomp.context_processors.debug_mode',
	'ocukphotocomp.photocomp.context_processors.photo_url',
	'ocukphotocomp.photocomp.context_processors.season_list',
	'django.contrib.auth.context_processors.auth',
)

MIDDLEWARE_CLASSES = (
#    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
#    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'ocukphotocomp.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    #! Don't forget to use absolute paths, not relative paths.
    #"/home/growse/django/templates",
)

INSTALLED_APPS = (
	'django.contrib.staticfiles',		
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'ocukphotocomp.photocomp',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'django.contrib.sitemaps',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'pipeline',
)

FORCE_SCRIPT_NAME = ''

CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
		'LOCATION': '/var/tmp/django_cache',
	}
}

CACHE_MIDDLEWARE_KEY_PREFIX='growse_com_photocomp'
CACHE_MIDDLEWARE_SECONDS=300

try:
	    from local_settings import *
except ImportError:
	    pass
