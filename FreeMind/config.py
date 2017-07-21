import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'FreeMind.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

mail = {
    "mailAdresses": {
        logging.INFO: ('daniel.koersten@posteo.de'),
        logging.WARN: ('valentin@boettcher.cf')
    },
    "mailServer": {
        "host": "igf-jena.de",
        "username": "m03f19d3",
        "password": "eN2QepkFcdaD"
    },
    "subjectLine": "Freemind Logging | %(levelname)s | Na dann mal ran an den Speck!"
}

warnings = {
    "full": "Die Festplatte: %s ist voll, na Toll."
}
