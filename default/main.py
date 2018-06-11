# [START imports]
from flask import Flask
from cache import cache

import config

from who import WHO
import sys
# [END imports]

reload(sys)
sys.setdefaultencoding('utf8')

# [START create_app]
app = Flask(__name__)
app.config.from_object(config)

# Generate a key using
# >>> import os
# >>> os.urandom(24)
app.secret_key = 'generate key from instructinos above'

cache.init_app(app)
# [END create_app]

app.register_blueprint(WHO, url_prefix='/api/who')

# [END app]
