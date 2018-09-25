import os
from logging.config import dictConfig


WATER_TANK_WEIGHT_MAX = 1000  # [g]
WATER_MIN_WEIGHT = 100  # [g]

BEANS_TANK_WEIGHT_MAX = 1000  # [g]
BEANS_MIN_WEIGHT = 50  # [g]


COFFEE_TYPES = {
    'AMERICANO': {
        'water_weight': 100,
        'beans_weight': 50
    },
    'CAPPUCCINO': {
        'water_weight': 50,
        'beans_weight': 40
    },
    'ESPRESSO': {
        'water_weight': 20,
        'beans_weight': 20
    },
    'DOPPIO': {
        'water_weight': 50,
        'beans_weight': 20
    }
}


BASE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))
LOG_DIRECTORY = os.path.join(BASE_DIR, 'logs')
LOGFILE_SIZE = 5 * 1024 * 1024
LOGFILE_COUNT = 5

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d] %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'general': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIRECTORY, 'general.log'),
            'formatter': 'verbose',
            'maxBytes': LOGFILE_SIZE,
            'backupCount': LOGFILE_COUNT
        }
    },
    'loggers': {
        'general': {
            'handlers': ['general', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

dictConfig(LOGGING)
