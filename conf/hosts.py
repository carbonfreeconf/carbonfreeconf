from django_hosts import patterns, host
from django.conf import settings
import os

if not 'ON_HEROKU' in os.environ:
    host_patterns = patterns('',
        host(r'www', settings.ROOT_URLCONF, name='www'),  # <-- The `name` we used to in the `DEFAULT_HOST` setting
        host(r'127', settings.ROOT_URLCONF, name='127'),
        host(r'(?!www).*', 'conf.hostconfs.urls', name='wildcard'),
    )
else:
    host_patterns = patterns('',
        host(r'www', settings.ROOT_URLCONF, name='www'),  # <-- The `name` we used to in the `DEFAULT_HOST` setting
        #host(r'default', 'my_app.urls', name='default'),
        #host(r'beta', 'my_app.urls', name='beta'),
        host(r'(?!www).*', 'conf.hostconfs.urls', name='wildcard'),
        #host(r'(\w+)', 'conf.hostconfs.urls', name='wildcard'),

    )


