SECRET_KEY = 'MY_SUPER_SECRET_KEY'

# Connection settings
SNOW_INSTANCE = ''
SNOW_OAUTH_CLIENT_ID = ''
SNOW_OAUTH_CLIENT_SECRET = ''


# Import pysnow logger
LOGGING = {
    'version': 1,
    'formatters': {
        'default': {'format': '[%(asctime)s %(name)s] %(message)s'}
    },
    'handlers': {
        'debug': {
            'level': 'DEBUG',
            'formatter': 'default',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'pysnow': {
            'handlers': ['debug'],
            'level': 'DEBUG'
        }
    }
}
