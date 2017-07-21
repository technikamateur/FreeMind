import time
import subprocess
from threading import Timer as _Timer, Lock

class Timer(_Timer):
    """
    See: https://hg.python.org/cpython/file/2.7/Lib/threading.py#l1079
    """

    def run(self):
        while not self.finished.is_set():
            self.finished.wait(self.interval)
            self.function(*self.args, **self.kwargs)

        self.finished.set()

class Action:
    """The action Base Class, with an Implementation for timers and caching. It has built-in support for running shell-scripts. All time intervalls are in Seconds."""
    # TODO: Persistence

    def runShellScript(self, scriptPath, *scriptArgs, sudo = False):
        try:
            su = ['sudo'] if sudo else []
            shellProcess = subprocess.run(sudo.append(["/bin/bash", scriptPath]).append(*scriptArgs), stdout=subprocess.PIPE)
            return shellProcess.stdout.decode('utf-8')
        except Error:
            return None

    def defaultAction():
        """A function which performs the Action. It is to be overwritten by the Subclass."""
        pass

    def run(self, force=False, *args, **kwargs):
        """Run the action and get the restult either Cached or New."""
        self.mutex.acquire()

        try:
            if force or self.result is None or (time.time() - self.lastExec) > self.cacheTime:
                self.result = defaultAction if self.action is None else self.action(*args, **kwargs)
                self.lastExec = time.time()

        finally:
            self.mutex.release()
            return self.result

    def __init__(self, action=None, updateInterval=None, cacheTime=None, scriptPath=None, scriptArgs=None, sudo=False):
        # Time between the auto-updates
        self.updateInterval = None if updateInterval is None else updateInterval

        # Time until cache is dropped
        self.cacheTime = 0 if cacheTime is None else cacheTime

        # The time of last execution
        self.lastExec = 0

        # A function which performs the Action. If it isn't set, the built in Method will be used.
        self.action = None if action is None else action

        self.action = (lambda: runScript(sudo, scriptPath, *scriptArgs))if self.action is None and scriptPath is not none else None

        # The return Value of the Action
        self.result = None

        self.mutex = Lock()

        if not self.updateInterval is None:
            self.timer = Timer(self.updateInterval, self.run)
            self.timer.start()
