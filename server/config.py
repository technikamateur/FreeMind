import logging
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
    "subjectLine": "Freemind Logging | %(levelname)s | Na dann mal ran an den Speck!",
    "interval": 10
}

warnings = {
    "full": "Die Festplatte: %s ist voll, na Toll."
}
