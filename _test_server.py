#!/usr/bin/env python2

from os import path
import shutil
import _tasks
from _manage import ROOT, CallTaskRunner, venv

v = venv()
VENV_PIP2 = path.join(v.path, 'bin', 'pip2')

storage_path = path.join(ROOT, ".storage.test")

TEST_SERVER = _tasks.DEV_APPSERVER(storage_path=storage_path, test=True)

# START THE TESTS
CallTaskRunner.run([TEST_SERVER])
shutil.rmtree(storage_path)

# npx cypress run --config baseUrl=http://localhost:8077 --env testService=http://localhost:8078
