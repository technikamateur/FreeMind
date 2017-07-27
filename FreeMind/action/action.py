""" TOPO - The Omni Present Observer

It observes. Actually it is just a collection of a handy framework for observing values
and running actions.

RTFM and be enlightened.
"""

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

class Observer(Object):
    """A class which provides basic monitoring methods and is inteded to be subclassed!
    When subclassing !!be sure to call __init__!!

    The errorMessages are a dictionary of which wonder, errorMessages.
    (Check `isError` and onError for details.)

    The methods implemented lay out an API for the Observer and provide handy and sufficient
    implementations for most use cases.
    """

    def isError(self, value):
        """Checks if the result is `None` or in the Error Dict.` If it is, it returns the
        value in the bellow-stated manner.

        In this implementation, the errorType is simply the value.
        This is Ok for operations which can either go good or bad and return a
        single (simple) Value.

        The errorType can be any Value which can be matched against a dictionary
        (see onError for the reason) and for the sake of simplicity and readibility
        a string is suggested. (Ex. SCARY_ERROR)

        This method should return tuple.
        The first element is an array composed of tuples in the form
        `(errorType, errorArgs)` where errorArgs is just an iterable of arguments containing
        additional information about the error. In the provided `onError` these arguments are
        supplied to the logger as values for the format string. Peanuts.

        The second element is the Number of errors which have been found.

        If everything went good and there is no error, just return `(False, False)`.
        """
        return False, False if value is None or value in self.errorMessag else \
            ([value], None)

    def onError(self, errors):
        """The default error handler invokes the app logger with the given Arguments.

        It expects an array of errors to handle.

        An error is represented by a tuple in the shape `(errorType, arguments)`
        where `arguments` is an iterable.
        """

        error = errors.pop()

        if len(errors) > 0:
            onError(errors)

        errorType, args = error

        err = self.errorMessages['default'] if errorType is None \
              or self.errorMessages[errorType] is None else self.errorMessages[errorType]

        logger.log(err['level'], err['message'], *args)

    def onSuccess(self):
        """A Proposal.

        You may want to Implement logging here.
        """
        raise NotImplementedError

    def observe(self, *args, **kwargs):
        """This method just comfortably combines the boilerplate of observing.
        Give it, what you would pass to the isError method and it automatically
        calls on error, if an error happened.

        In all other ways it behaves like `isError`."""
        error, numErr = self.isError(*args, **kwargs)

        if not error is False:
            self.onError(error, multiple=numErr)

        return error, numErr

    def __init__(self, errorMessages=None, *args, **kwargs):
        # A dictionary with errors and log-reactions.
        self.errorMessages = copy.deepcopy(errorHandlingConfig["defaultErrorMessages"])

        if not errorMessages is None:
            for key in errorMessages:
                self.errorMessages[key] = errorMessages[key]

class PersistentProperty(object):
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

class ObservedPersistentProperty(Observer, PersistentProperty):
    """A PersistentProperty child with _errorHandling.
    The value can either represent success, or a failure.
    This represents a very common special case of a property.
    The model which is being used must contain a `success` key as keyword Argument.

    This class is really only to be used for single valued properties.
    If you want fancier properties, be sure to overwrite the isError method.
    """

    def set(self, *args, **kwargs):
        error, errorType = self.isError(*args, **kwargs)[0]

        if error:
                self.onError(errorType, *args)

        PersistentProperty.set(self, success=not error, *args, **kwargs)

        if not error:
            self._lastSuccesfull = self._value

    def getLastSuccessfull(self):
        """Get the last successfull value of the property."""
        return self._lastSuccesfull

    def __init__(self, model, *args, **kwargs):
        """Inititalize with Keyword arguments for savety!"""
        if not hasattr(model, 'success'):
            raise ValueError('The Data Base Model must contain a `success` key!')

        PersistentProperty.__init__(self, model, *args, **kwargs)
        Observer.__init__(self, **kwargs)

        self._lastSuccesfull = self._getLatestFromDb(success=True)

# TODO: Support for Multiple Simultaneous Errors...
class Action(Observer):
    """This is a Class, intended to be subclassed!
    At least the action Method should be overwritten.

    An Object of this class represents an action, which is run and then observed.
    The result is being cached.
    Also a timer, which runs the action like a cron job is implemented and works --out of the box--.
    The basic interface is the get() method.

    There are some handy methods available to use at your disposal.

    It is also handy to use a dictionary for configuration and pass it as **kwargs.
    """

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

    def action(self):
        """A function which performs the Action.
        It is to be overwritten by the Subclass."""
        raise NotImplementedError()

    def _getResult(self):
        return self.result

    def _setResult(self, result):
        self.result = result

    def run(self, force=False, *args, **kwargs):
        """Run the action and get the restult either Cached or New.

        Returns the result and the errors which might have occurred in the `isError` format."""

        tmpResult = None

        if force or self._getResult is None \
           or (time.time() - self.lastExec) > self.cacheTime:
            tmpResult = self.action(*args, **kwargs)

            if(not tmpResult is None):
                self._setResult(tmpResult)
                self.lastExec = time.time()

            self.errors = self.isError(tmpResult)

        else:
            tmpResult = self._getResult()

        if not error is False:
            self.onError(error, errorDetails, tmpResult)

        return tmpResult, self.errors

    def __init__(self, updateInterval=None, cacheTime=None, *args, **kwargs):
        # Init error Handling
        super().__init__(**kwargs)

        # Time between the auto-updates
        self.updateInterval = None if updateInterval is None else updateInterval

        # Time until cache is dropped
        self.cacheTime = 0 if cacheTime is None else cacheTime

        # The time of last execution
        self.lastExec = 0

        # The return Value of the Action
        self.result = None
        self.errors = False, False

        if not self.updateInterval is None:
            scheduler.add_job(func=self.run,
                              trigger=IntervalTrigger(
                                  seconds=self.updateInterval))

class PersistentAction(Action):
    """Look! An action which is persistent! Use the PersistentProperty API to use the Persistency features, to keep it clean."""
    def _getResult(self):
        return self.result.get()

    def _setResult(self, value):
        self.result.set(value)

    def  __init__(self, discard=False, orderKey=None, *args, **kwargs):
        if self.model is None:

        super().__init__(*args, **kwargs)
        self.result = PersistentProperty(model, discard=discard, orderKey=orderKey)
