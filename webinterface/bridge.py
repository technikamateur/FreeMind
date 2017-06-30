import sys
sys.path.insert(0, '../server')
import config
import libary

def handleOsUpdate(status):
    if status == 'SUCCESS':
        libary.insert_actionlog(2, 1)
        libary.logger.info('OS Update PI.')
    else:
        libary.logger.error('OS Update auf PI fehlgeschlagen.')

    return 'OK'

def handleUpdate(status):
    if status == 'SUCCESS':
        libary.insert_actionlog(2, 2)
        libary.logger.info('FM Update PI.')
    else:
        libary.logger.error('FM Update auf PI fehlgeschlagen.')

    return 'OK'

def handleBackup(status):
    if status == 'SUCCESS':
        libary.insert_actionlog(2, 3)
        libary.logger.info('PI Backup Done.')
    else:
        libary.logger.error('PI Backup fehlgeschlagen.')

    return 'OK'

def doBackUp():
    try:
        hddname, mempercent, smart = libary.spacegrabber()
    except:
        return 'False'

    for hdd in range(0, len(hddname)):
        if mempercent[hdd] > 90 or smart[hdd] != 'passed':
            return 'False'

    return 'True'

def handleHddError():
    libary.logger.error('PI HDD ist im eimer! So ein Mist. Backup Futsch.')
    return 'OK'
