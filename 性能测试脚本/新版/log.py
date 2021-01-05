"""
    #  @ModuleName: logging
    #  @Function: 
    #  @Author: Ljx
    #  @Time: 2020/10/22 14:47
"""

import logging.handlers

logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

# rf_handler = logging.handlers.TimedRotatingFileHandler('logs/all.log', when='midnight', interval=1, backupCount=7,
#                                                        atTime=datetime.time(0, 0, 0, 0))
# rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

f_handler = logging.FileHandler('logs/error.log')
f_handler.setLevel(logging.DEBUG)
f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

# logger.addHandler(rf_handler)
logger.addHandler(f_handler)

logger.debug('debug message')
logger.info('info message')
logger.warning('warning message')
logger.error('error message')
logger.critical('critical message')