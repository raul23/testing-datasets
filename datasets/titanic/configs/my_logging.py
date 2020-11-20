logging = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters":
    {
        "console":
        {
          "format": "[%(name)s] %(message)s"
        },
        "simple":
        {
          "format": "%(levelname)-8s %(message)s"
        },
        "verbose":
        {
          "format": "%(asctime)s | %(name)-42s | %(levelname)-8s | %(message)s"
        }
    },

    "handlers":
    {
        "console":
        {
          "level": "INFO",
          "class": "logging.StreamHandler",
          "formatter": "simple"
        },
        "file":
        {
          "level": "INFO",
          "class": "logging.FileHandler",
          "filename": "debug.log",
          "mode": "a",
          "formatter": "simple",
          "delay": True
        }
    },

    "loggers":
    {
        "darth_vader_rpi.darth_vader":
        {
          "level": "INFO",
          "handlers": ["console"],
          "propagate": False
        },
        "darth_vader_rpi.ledutils":
        {
          "level": "INFO",
          "handlers": ["console"],
          "propagate": False
        },
        "darth_vader_rpi.start_dv":
        {
          "level": "INFO",
          "handlers": ["console"],
          "propagate": False
        },
        "SimulRPi.GPIO":
        {
          "level": "INFO",
          "handlers": ["console"],
          "propagate": False
        },
        "SimulRPi.manager":
        {
          "level": "INFO",
          "handlers": ["console"],
          "propagate": False
        }
    },

    "root":
        {
          "level": "INFO",
          "handlers": ["console"],
          "propagate": False
        }
}
