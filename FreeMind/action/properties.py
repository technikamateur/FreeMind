from FreeMind.action import PersistentProperty, ObservedPersistentProperty
from FreeMind.models import PiOsUpdate, PiFmUpdate, PiHddStatus, Backup
from FreeMind.config import propertiesConfig

class Pi():
    __config = propertiesConfig['Pi']
    osUpdate = ObservedPersistentProperty(PiOsUpdate, **__config['osUpdate'])
    freeMindUpdate = ObservedPersistentProperty(PiFmUpdate, **__config['freeMindUpdate'])
    hddStatus = ObservedPersistentProperty(PiHddStatus, **__config['hddStatus'])

class Master():
    __config = propertiesConfig['Master']
    backup = ObservedPersistentProperty(Backup, **__config['backup'])
