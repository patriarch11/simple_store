import sys

from loguru     import logger

from src.config    import settings
from src.constants import LOG_FORMAT

def configure_logger():
	logger.remove()

	logger.add(
		sys.stdout,
		level    = 'INFO',
		format   = LOG_FORMAT,
		colorize = True,
	)
	if settings.DEBUG:
		logger.add(
			sys.stdout,
			level = 'DEBUG',
			format = LOG_FORMAT,
			colorize = True,
		)
