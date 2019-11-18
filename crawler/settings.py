import os
import logging.config


FILES_LIMIT = int(os.getenv('FILES_LIMIT', '30000'))
SITE_URL = os.getenv('SITE_URL', 'https://www.softpedia.com/')

BASE_DIR = os.getenv('BASE_DIR', os.path.dirname(os.path.abspath(__file__)))
ARCHIVES_DIR = os.path.join(BASE_DIR, 'archives')

SUPPORTED_7ZIP_FORMATS = (
    'application/zip',
    'application/x-tar',
)

DEBUG = os.getenv('DEBUG') == '1'
LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s %(name)-15s '
                      '%(levelname)-8s %(processName)-10s %(message)s'
        },
        'simple': {
            'class': 'logging.Formatter',
            'format': '%(name)-15s %(levelname)-8s '
                      '%(processName)-10s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': LOG_LEVEL,
            'formatter': 'detailed',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': LOG_LEVEL,
    },
}


logging.config.dictConfig(LOGGING)
