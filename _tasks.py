from os import path
from _manage import ROOT, CallTask

storage_path = path.join(ROOT, ".storage")

CLEAN = CallTask(ROOT, ['yarn', 'clean'])


def DEV_APPSERVER(storage_path=storage_path, test=False):
    task_args = ["dev_appserver.py", "--storage_path=%s" % storage_path]
    if test:
        task_args += ["--clear_datastore", "--admin_port=8076", "--port=8077"]
    else:
        task_args += [
            "--log_level=debug", "--enable_console", "--host=0.0.0.0"
        ]

    task_args += [
        path.join(ROOT, "default", "app.yaml"),
        # path.join(ROOT, "default", "test.yaml")
    ]

    return CallTask(ROOT, task_args)


DEPENDENCIES = CallTask(ROOT, ['yarn', 'deps'])

WEB_START = CallTask(path.join(ROOT, "web"), ["yarn", "start"])
WEB_BUILD = CallTask(path.join(ROOT, 'web'), ["yarn", "build"])
