import os
import logging
import logging.config


ROOT_LEVEL = os.environ.get('PROD', "INFO")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
        "critical_filehandler": {
            "level": "CRITICAL",
            "formatter": "standard",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/server_critical.log"
        },
        "error_filehandler": {
            "level": "CRITICAL",
            "formatter": "standard",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/server_error.log"
        }
    },
    "loggers": {
        "": {  # root logger
            "level": ROOT_LEVEL, #"INFO",
            "handlers": ["default"],
            "propagate": False,
        },
        "": {
            "level": "CRITICAL",
            "handlers": ['critical_filehandler']
        },
        "": {
            "level": "ERROR",
            "handlers": ['error_filehandler']
        },
        "uvicorn.error": {
            "level": "DEBUG",
            "handlers": ["default"],
        },
        "uvicorn.access": {
            "level": "DEBUG",
            "handlers": ["default"],
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)