#!/usr/bin/env python2
import os
from os.path import dirname
import subprocess
from threading import Thread

import logging

UTIL = dirname(os.path.realpath(__file__))
ROOT = dirname(UTIL)


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
