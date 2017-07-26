import time
import subprocess
import logging
import atexit
import copy
from FreeMind import db
from FreeMind import app
from FreeMind.config import actionConfig, errorHandling as errorHandlingConfig
from FreeMind.logger import logger
from sqlalchemy.inspection import inspect
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

# TODO: Use Exceptions for Error handling!

# Set Up Timer
scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(scheduler.shutdown)

class _ErrorHandling(object):
    def defaultIsError(self, value):
        """Checks if the result is `None` or in the Error Dict.`"""
        return value is None or value in self.errorMessages, value

    def defaultOnError(self, errorType, *args):
        """The default error handler invokes the app logger."""

        err = self.errorMessages['default'] if errorType is None \
              or self.errorMessages[errorType] is None else self.errorMessages[errorType]


        # TODO: nicer
        if args[0] is None:
            logger.log(err['level'], err['message'])
        else:
            logger.log(err['level'], err['message'], *args)

    def __init__(self, errorMessages=None, onError=None, isError=None, *args, **kwargs):
         # A function which is invoked if an error Value is returned by the action.
        self.onError = self.defaultOnError if onError is None else onError

        # A function that evaluates, if the the result of the Action is an Error
        self.isError = self.defaultIsError if isError is None else isError

        # A dictionary with errors and log-reactions.
        self.errorMessages = copy.deepcopy(errorHandlingConfig["defaultErrorMessages"])

        if not errorMessages is None:
            for key in errorMessages:
                self.errorMessages[key] = errorMessages[key]

class DataBaseProperty(object):
    """A Class to manage Properties, which are obtained across time and therefore are sortable (preferably with a timestamp)."""
    def get(self):
        return self._value

    def set(self, *args, **kwargs):
        with app.app_context():
            # Delete All
            if self.discard:
                db.session.delete(self.getAll())

            tmp = self.model(*args, **kwargs)
            db.session.add(tmp)
            db.session.commit()

            self._value = db

    def _getLatestFromDb(self, **filters):
        with app.app_context():
            tmp = self.model.query.filter_by(**filters).order_by(self.orderKey.desc()).first()

            if self.serialized:
                tmp = [self.model.deSerialize(deSerialized) for deSerialized in tmp]

            return tmp

    def getAll(self, **filters):
        with app.app_context():
            return self.model.query.filter_by(**filters).all()

    def __init__(self, model, orderKey=None, discard=False, *args, **kwargs):
        """orderKey is Optional, the primary key is used by default."""
        self.model = model
        self.orderKey = inspect(model).primary_key[0] if orderKey is None else orderKey
        self.discard = discard
        self.serialized = hasattr(model, 'deSerialize') # TODO: Better Implementation
        self._value = self._getLatestFromDb()

class BinaryDBProperty(_ErrorHandling, DataBaseProperty):
    """A DataBaseProperty child with _errorHandling.
    The value can either represent success, or a failure (thus binary).
    This represents a very common special case of a property.
    The model which is being used must contain a `success` key as keyword Argument."""

    def set(self, *args, **kwargs):
        error, errorType = self.isError(*args, **kwargs)

        if error:
            if len(kwargs) > 0:
                self.onError(errorType, kwargs, *args)
            else:
                self.onError(errorType, *args)

        DataBaseProperty.set(self, success=not error, *args, **kwargs)

        if not error:
            self._lastSuccesfull = self._value
            pass

    def getLastSuccessfull(self):
        """Get the last successfull value of the property."""
        return self._lastSuccesfull

    def __init__(self, model, *args, **kwargs):
        """Inititalize with Keyword arguments for savety!"""
        if not hasattr(model, 'success'):
            raise ValueError('The Data Base Model must contain a `success` key!')

        DataBaseProperty.__init__(self, model, *args, **kwargs)
        _ErrorHandling.__init__(self, **kwargs)

        self._lastSuccesfull = self._getLatestFromDb(success=True)

# TODO: Support for Multiple Simultaneous Errors...
class Action(_ErrorHandling):
    """The action Base Class, with an Implementation for timers and caching.
    The action is a function which returns a Value in case of success or `None` otherwise.
    It has built-in support for running shell-scripts. All time intervalls are in Seconds."""
    # TODO: Persistence

    def runExternal(self, commandPath, sudo = False, *commandArgs):
        """Runs a given shell script and returns STDOUT.
        It returns None on error."""

        command = ['/usr/bin/sudo'] if sudo else []
        command.append(commandPath)
        command.extend(commandArgs)

        try:
            shellProcess = subprocess.run(command, stdout=subprocess.PIPE)

            return shellProcess.stdout.decode('utf-8')

        except subprocess.CalledProcessError:
            return None

    def defaultAction(self):
        """A function which performs the Action.
        It is to be overwritten by the Subclass."""
        return None

    def _getResult(self):
        return self.result

    def _setResult(self, result):
        self.result = result

    def run(self, force=False, *args, **kwargs):
        """Run the action and get the restult either Cached or New."""

        error = False
        tmpResult = None
        errorDetails = False

        try:
            if force or self._getResult is None \
               or (time.time() - self.lastExec) > self.cacheTime:
                tmpResult = self.action(*args, **kwargs)

                if(not tmpResult is None):
                    self._setResult(tmpResult)
                    self.lastExec = time.time()

            else:
                tmpResult = self._getResult()

        finally:
            if tmpResult is None:
                error, errorDetails = 'ACTION_FAILED', None
            else:
                error, errorDetails = self.isError(tmpResult)

            if not error is False:
                self.onError(error, errorDetails, tmpResult)

        return tmpResult, error, errorDetails

    def __init__(self, action=None, updateInterval=None, cacheTime=None, commandPath=None,
                 commandArgs=None, sudo=False, *args, **kwargs):
        # Init error Handling
        super().__init__(**kwargs)

        # Time between the auto-updates
        self.updateInterval = None if updateInterval is None else updateInterval

        # Time until cache is dropped
        self.cacheTime = 0 if cacheTime is None else cacheTime

        # The time of last execution
        self.lastExec = 0

        # A function which performs the Action.
        # If it isn't set, the built in Method will be used.
        self.action = self.defaultAction if action is None else action

        # Use a Shell Script if provided.
        if not action is None:
            self.action = action

        elif not commandPath is None:
            cArgs = [] if commandArgs is None else commandArgs
            self.action = lambda: self.runExternal(commandPath, sudo, *cArgs)

        else:
            self.action = self.defaultAction

        # The return Value of the Action
        self.result = None

        if not self.updateInterval is None:
            scheduler.add_job(func=self.run,
                              trigger=IntervalTrigger(
                                  seconds=self.updateInterval))

class PersistentAction(Action):
    """Look! An action which is persistent! Use the DataBaseProperty API to use the Persistency features, to keep it clean."""
    def _getResult(self):
        return self.result.get()

    def _setResult(self, value):
        self.result.set(value)

    def  __init__(self, model, discard=False, orderKey=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = DataBaseProperty(model, discard=discard, orderKey=orderKey)
