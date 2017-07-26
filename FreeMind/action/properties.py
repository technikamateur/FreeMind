from FreeMind.action import DataBaseProperty, BinaryDBProperty
from FreeMind.models import PiOsUpdate, PiFmUpdate, PiHddStatus, Backup
from FreeMind.config import propertiesConfig

class Pi():
    __config = propertiesConfig['Pi']
    osUpdate = BinaryDBProperty(PiOsUpdate, **__config['osUpdate'])
    freeMindUpdate = BinaryDBProperty(PiFmUpdate, **__config['freeMindUpdate'])
    hddStatus = BinaryDBProperty(PiHddStatus, **__config['hddStatus'])

class Master():
    __config = propertiesConfig['Master']
    backup = BinaryDBProperty(Backup, **__config['backup'])
