from FreeMind import app
from flask import request
from FreeMind.action.actions import getHddHealth, getHddSpace
from FreeMind.action.properties import Pi, Master

@app.route('/bridge', methods=['GET'])
def handleBridge():
    action = request.args.get('action')
    status = request.args.get('status')

    if action is None or status is None:
        return "Invalid Request"

    returnStatus = "OK"

    if action == "OS_UPDATE":
        Pi.osUpdate.set(status)

    elif action == "FM_UPDATE":
        Pi.freeMindUpdate.set(status)

    elif action == "BACKUP":
        Master.backup.set(status)

    elif action == "DO_BACKUP":
        returnStatus = shouldDoBackUp()

    elif action == "HDD_STATUS":
        Pi.hddStatus.set(status)

    return returnStatus

def shouldDoBackUp():
    space, spaceError, spaceErrorDetails = getHddSpace.run() # TODO: more elegant
    health, healthError, healthErrorDetails = getHddHealth.run()

    return "False" if spaceError or healthError else "True"
