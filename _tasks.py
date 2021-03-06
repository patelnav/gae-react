from os import path
from __init__ import CONFIG, ROOT, CallTask

CLEAN = CallTask(ROOT, ['yarn', 'clean'])


def DEV_APPSERVER(storage_path, datastore_emulator = None, test=False):
    task_args = ["dev_appserver.py", "--storage_path=%s" % storage_path]
    if test:
        task_args += ["--clear_datastore", "--admin_port=8076", "--port=8077"]
    else:
        task_args += [
            "--log_level=debug", "--enable_console", "--host=0.0.0.0"
        ]

    if datastore_emulator if datastore_emulator != None else CONFIG.DATASTORE_EMULATOR:
        task_args += ["--support_datastore_emulator=true", "--application field-scope"]

    task_args += [
        path.join(CONFIG.SERVER_PATH, "app.yaml"),
    ]

    test_yaml = path.join(CONFIG.SERVER_PATH, "test.yaml")
    if path.exists(test_yaml):
        task_args += [test_yaml]

    for addl_yaml in CONFIG.ADDL_YAMLS:
        if path.exists(addl_yaml):
            task_args += [addl_yaml]

    return CallTask(ROOT, task_args)


DEPENDENCIES = CallTask(ROOT, ['yarn', 'deps'])

WEB_START = CallTask(CONFIG.WEB_PATH, ["yarn", "start"])
WEB_BUILD = CallTask(CONFIG.WEB_PATH, ["yarn", "build"])
