from FreeMind.action import Action
from FreeMind.config import hddList, actionConfig, baseDir
from FreeMind import properties
import time
import re
import os

class __HddSpace(Action): # TODO: better error checking...
    def action(self):
        # get disk usage
        df = self.runExternal('df').split('\n')

        if df is None:
            return None

        df = list(map(lambda row: re.split(' +', row), df))
        df = list(filter(lambda row: row[0] in hddList, df))

        if len(df) is 0:
            return None

        space = {
            hdd: {
                'total': int(d[1]),
                'free': int(d[3]),
                'full': 100 - int((int(d[3])/int(d[1])) * 100), # TODO: more efficient
                'mount': d[5]
            } for hdd in hddList for d in df if d[0] == hdd}

        return space

    def isError(self, result):
        if result is None: # TODO: There may be a more elegant way.
            return [('ACTION_FAILED', ('Unknown Cause.')),]

        errors = [('ACTION_FAILED', (hdd)) for hdd in hddList if hdd not in result]

        fullHdd = [('HDD_FULL', (hdd)) for hdd in result if \
                            (result[hdd]['full']) > hddList[hdd]['maxFull']]

        errors.extend(fullHdd)

        return False if len(errors) is 0 else errors

    def __init__(self):
        super().__init__(**actionConfig['hddSpace'])

class __HddHealth(Action):
    def action(self):
        health = {hdd: self.runExternal('/usr/bin/smartctl -H ', hdd, sudo=True) \
                     for hdd in hddList}

        for hdd in health:
            # Remove the trailing \n
            tmpHealth = self.healthRe.findall(health[hdd])
            health[hdd] = None if len(tmpHealth) < 1 else tmpHealth[0]

        return health

    def isError(self, result):
        if result is None: # TODO: There may be a more elegant way.
            return [('ACTION_FAILED', ('Unknown Cause.')),]

        errors = [('ACTION_FAILED', (hdd)) for hdd in hddList if (hdd not in result) or (result[hdd] is None)]

        badHealt = [('HDD_ILL', (hdd, result[hdd])) for hdd in result if result[hdd] != 'PASSED' and hdd not in [error[1] for error in errors]]

        errors.extend(badHealt)

        return False if len(errors) is 0 else errors

    def __init__(self):
        super().__init__(**actionConfig['hddHealth'])
        self.healthRe = re.compile(' result: ([A-Z]+)\n')

class __isBackUpOverDue(Action):
    def action(self):
        return properties.Master.backup.getLastSuccessfull()

    def isError(self, backup):
        if time.time() - backup.time > self.maxBackupInterval:
            return [('BACKUP_OVERDUE')]
        else:
            return False

    def __init__(maxBackupInterval, *args, **kwargs):
        self.maxBackupInterval = maxBackupInterval
        super().__init__(*args, **kwargs)

# Export the Handlers
getHddSpace = __HddSpace()
getHddHealth = __HddHealth()
__backupWatcher = __isBackUpOverDue(**actionConfig['isBackupOverDue'])
# NOTE: You could wrap this into multiple Actions, but leave them like this, to enable a more flexible config.

def getHddSumary():
    """A Little Helper, to prepare the data for the view."""
    space, errors = getHddSpace.run()
    health, healthErrors = getHddHealth.run()

    errors = errors if not errors is False else []

    if healthErrors:
        errors.extend(healthErrors)

    hdds = {}

    for hdd in hddList:
        if not (space is None or space.get(hdd) is None):
            hdds[hdd] = space[hdd]
        else:
            hdds[hdd] = {}

        if not (space is None or health.get(hdd)is None):
            hdds[hdd]['health'] = health[hdd]

        hdds[hdd]['name'] = hddList[hdd]['name']

        hdds[hdd]['color'] = 'green'

        for error, errorDetails in errors:
            if errorDetails is hdd:
                if error is 'ACTION_FAILED':
                    hdds[hdd]['offline'] = True
                    hdds[hdd]['color'] = 'red'
                    break

                hdds[hdd]['color'] = 'red' if error is 'HDD_ILL' else 'yellow' \
                                 if error is 'HDD_FULL' else 'gray'

    return hdds
