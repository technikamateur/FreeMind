import os
import logging

baseDir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(baseDir, 'FreeMind.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

mail = {
    "mailAdresses": {
        #logging.INFO: ('daniel.koersten@posteo.de'),
        logging.WARN: ('valentin@boettcher.cf')
    },
    "mailServer": {
        "host": "igf-jena.de",
        "username": "m03f19d3",
        "password": "eN2QepkFcdaD"
    },
    "subjectLine": "Freemind Logging | %(levelname)s | Na dann mal ran an den Speck!",
    "interval": 10,
 }

errorMessa = {
    "full": "Die Festplatte: %s ist voll, na Toll."
}

hddList = {
    "/dev/sda1": {
        "maxFull": 90,
        "name": "boot"
    },
    "/dev/sda2": {
        "maxFull": 90,
        "name": "main"
    },
    "/dev/sdd": {
        "maxFull": 90,
        "name": "main"
    }
}

errorHandling = {
    "defaultErrorMessages":  {
            "default": {
                "message": "Ein unbekannter Fehler ist aufgetreten. %",
                "level": logging.ERROR
            },
            "ACTION_FAILED": {
                "message": "Aktion Fehlgeschlagen!",
                "level": logging.ERROR
            }
    }
}

# Configuration for the Actions. The dict gets converted into KWArgs! The action.errorMessages key gets merged with the Error messages of all other error messages.
actionConfig = {
    "hddSpace": {
        "updateInterval": 1,
        "cacheTime": 0,
        "repeatInterval": 10,
        "errorMessages": {
            "ACTION_FAILED": {
                "message": "Konnte HDD (%s) Fuellstand nicht abrufen!",
                "level": logging.ERROR
            },
            "HDD_FULL": {
                "message": "Die Festplatte/n %s ist/sind Voll! Status: %s",
                "level": logging.WARN
            },
        }
    },
    "hddHealth": {
        "updateInterval": 15,
        "cacheTime": 10,
        "errorMessages": {
            "ACTION_FAILED": {
                "message": "Konnte HDD ()Status nicht abrufen!",
                "level": logging.ERROR
            },
            "HDD_ILL": {
                "message": "Die Festplatte/n %s ist/sind in keinem guten Zustand! Status: %s",
                "level": logging.WARN
            }
        }
    }
}

propertiesConfig = {
    "Pi": {
        "osUpdate": {
            "errorMessages": {
                "FAILED": {
                    "message": "Pi OS Update fehlgeschlagen. %s",
                    "level": logging.WARN
                }
            }
        },
        "freeMindUpdate": {
            "errorMessages": {
                "FAILED": {
                    "message": "Pi FreeMind Update fehlgeschlagen. %s",
                    "level": logging.WARN
                }
            }
        },
        "hddStatus": {
            "errorMessages": {
                "ERROR": {
                    "message": "Raspberry Pi HDD is DEFEKT! Keine Backups Moeglich. %s",
                    "level": logging.ERROR
                }
            }
        }
    },
    "Master": {
        "backup": {
            "errorMessages": {
                "FAILED": {
                    "message": "Backup Fehlgeschlagen. %s",
                    "level": logging.WARN
                }
            }
        },
        "freeMindUpdate": {
            "errorMessages": {
                "FAILED": {
                    "message": "Pi FreeMind Update fehlgeschlagen. %s",
                    "level": logging.WARN
                }
            }
        }
    }
}
