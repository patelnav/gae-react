import os

CACHE_TYPE = 'gaememcached'

if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
    # Production
    IN_PRODUCTION = True
else:
    IN_PRODUCTION = False
