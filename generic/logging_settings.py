from generic import settings
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },
        },
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            #'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'class': 'generic.logging.TimedRotatingFileHandler',
            'filename': BASE_DIR+'/logs/hackathon.log',
            'when': 'midnight',
            'backupCount': 30,
            'formatter': 'default'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'hackathon': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}