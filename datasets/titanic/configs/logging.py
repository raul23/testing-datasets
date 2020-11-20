logging = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters":
    {
        "console":
        {
          "format": "[%(name)s] | %(levelname)-8s | %(message)s"
        },
        "only_msg":
        {
          "format": "%(message)s"
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
          "level": "DEBUG",
          "class": "logging.StreamHandler",
          "formatter": "console"
        },
        "console_only_msg":
        {
          "level": "DEBUG",
          "class": "logging.StreamHandler",
          "formatter": "only_msg"
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
        "datasets.titanic.data_exploration":
        {
          "level": "DEBUG",
          "handlers": ["console"],
          "propagate": False
        },
        "datasets.my_utils.dautils":
        {
          "level": "DEBUG",
          "handlers": ["console_only_msg"],
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
