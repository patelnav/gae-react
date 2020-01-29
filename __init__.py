#!/usr/bin/env python2
import os
from os import path
import subprocess
from threading import Thread
import json
import logging

UTIL = path.dirname(path.realpath(__file__))
ROOT = path.dirname(UTIL)

with open(path.join(ROOT, 'package.json'), 'r') as f:
    package_json = json.load(f)


class Config(object):
    PROJECT_ID = None
    SERVER_PATH = None
    WEB_PATH = None
    ADDL_YAMLS = []
    DATASTORE_STORAGE_PATH = None
    DATASTORE_EMULATOR = None

    def __init__(self, package_json):
        self.PROJECT_ID = package_json['project-id']
        self.SERVER_PATH = path.join(ROOT, package_json['server-folder'])
        self.WEB_PATH = path.join(ROOT, package_json['web-folder'])
        self.DATASTORE_STORAGE_PATH = package_json.get('datastore-storage-path',
                                                       path.join(ROOT, ".storage"))
        self.DATASTORE_EMULATOR = package_json.get('datastore-emulator', False)
        
        ays = []
        for ay in package_json.get('additional-yamls', []):
            ays.append(path.join(ROOT, ay))
        
        self.ADDL_YAMLS = ays



CONFIG = Config(package_json['gae-react'])


class CallTask(object):
    """Task to be called with subprocess.call"""
    proc = None

    def __init__(self, cwd, command):
        self.cwd = cwd
        self.command = command

    def __repr__(self):
        return " ".join(self.command)

    def run(self):
        self.proc = subprocess.Popen(str(self),
                                     cwd=self.cwd,
                                     shell=True,
                                     preexec_fn=os.setsid)

        print("\nStarted PID:{proc.pid}:\n\t{cmd}".format(proc=self.proc,
                                                          cmd=self))

        self.proc.communicate()

        print("""Completed {proc.pid} (Code: {proc.returncode}):
        \n\t{cmd}""".format(proc=self.proc, cmd=self))

        if self.proc.returncode != 0:
            raise Exception("Non-zero return code (%s)" % self.proc.returncode,
                            self)

    def kill(self):
        print("\nKilling %s" % self)
        import signal
        if not self.proc:
            print("No process to kill for", self)
        else:
            try:
                print("Trying to kill PID: %s" % self.proc.pid)
                os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
                self.proc.wait()
            except Exception as e:
                print(e)


class CallTaskRunner(object):
    @staticmethod
    def run(tasks):
        threads = []
        try:
            for task in tasks:
                thread = Thread(target=task.run)
                # thread.daemon = True
                thread.start()
                threads.append((thread, task))

            for thread, task in threads:
                while thread.isAlive():
                    thread.join(1)
                if task.proc.returncode != 0:
                    raise Exception(
                        "Non-zero return code (%s)" % task.proc.returncode,
                        task)

        except KeyboardInterrupt:
            logging.info('Keyboard Interrupt')
            for thread, task in threads:
                while thread.isAlive():
                    task.kill()
                if task.proc.returncode != 0:
                    raise Exception(
                        "Non-zero return code (%s)" % task.proc.returncode,
                        task)


class venv(object):
    def __init__(self):
        p = subprocess.Popen('./venv -p',
                             cwd=UTIL,
                             stdout=subprocess.PIPE,
                             shell=True)

        self.path = p.communicate()[0].strip()


VENV = venv()
