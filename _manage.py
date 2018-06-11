from os import path
import subprocess
from threading import Thread
from Queue import Queue

import logging

ROOT = path.dirname(path.realpath(__file__))


class CallTask(object):
    """Task to be called with subprocess.call"""

    def __init__(self, cwd, command):
        self.cwd = cwd
        self.command = command

    def __repr__(self):
        return " ".join(self.command)


class CallTaskRunner(object):
    @staticmethod
    def run(tasks):
        q = Queue()

        def worker():
            while True:
                task = q.get()
                try:
                    p = subprocess.Popen(
                        str(task),
                        cwd=task.cwd,
                        shell=True)
                    p.communicate()

                finally:
                    q.task_done()

        for i in range(len(tasks)):
            t = Thread(target=worker)
            t.daemon = True
            t.start()

        logging.info('Running tasks [%i]:' % len(tasks))

        for task in tasks:
            logging.info("\t%s" % task)
            q.put(task)

        q.join()


class venv(object):
    def __init__(self):
        subprocess.call('./venv', cwd=ROOT, shell=True)

        p = subprocess.Popen(
            './venv -p', cwd=ROOT, stdout=subprocess.PIPE, shell=True)

        self.path = p.communicate()[0].strip()
