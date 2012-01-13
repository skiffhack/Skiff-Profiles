from .common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_PATH, 'database', 'db.sqlite'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

BASE_DOMAIN = 'lvh.me:8000'

# Debug toolbar
try:
    import debug_toolbar
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)
    INTERNAL_IPS = ('127.0.0.1',)
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }
except ImportError:
    pass

try:
    import devserver
    INSTALLED_APPS += ('devserver',)
    
    DEVSERVER_MODULES = (
        'devserver.modules.sql.SQLRealTimeModule',
        'devserver.modules.sql.SQLSummaryModule',
        'devserver.modules.profile.ProfileSummaryModule',

        # Modules not enabled by default
        'devserver.modules.ajax.AjaxDumpModule',
        'devserver.modules.profile.MemoryUseModule',
        'devserver.modules.cache.CacheSummaryModule',
        'devserver.modules.profile.LineProfilerModule',
        )
    
    #DEVSERVER_IGNORED_PREFIXES = ['/media', '/uploads']
except ImportError:
    pass
    
