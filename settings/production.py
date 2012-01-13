from .common import *
import os, sys, urlparse
urlparse.uses_netloc.append('postgres')
urlparse.uses_netloc.append('mysql')
try:
    if os.environ.has_key('DATABASE_URL'):
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        DATABASES['default'] = {
            'NAME':     url.path[1:],
            'USER':     url.username,
            'PASSWORD': url.password,
            'HOST':     url.hostname,
            'PORT':     url.port,
        }
        if url.scheme == 'postgres':
            DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
        if url.scheme == 'mysql':
            DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'
except:
    print "Unexpected error:", sys.exc_info()
