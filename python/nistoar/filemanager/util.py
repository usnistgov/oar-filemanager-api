import logging
import os
import sys
import tempfile
from loguru import logger


def disable_fastapi_logging():
    uvicorn_error = logging.getLogger("uvicorn.error")
    uvicorn_error.disabled = True
    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_access.disabled = True


NONE_LOG_LEVEL = "NONE"


def initialize_logger(name, log_level):
    logger.remove()
    
    if log_level == NONE_LOG_LEVEL:
        logger.disable(name)
        return
    
    # Loguru default logging format
    # "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    if log_level == "DEBUG":
        log_format = "<yellow>{time:YYYY-MM-DD at HH:mm:ss}</yellow> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    else:
        log_format = "<yellow>{time:YYYY-MM-DD at HH:mm:ss}</yellow> | <level>[{level}]</level> {message}"

    logger.add(sys.stdout, colorize=True, format=log_format, level=log_level)
    logger.enable(name)


def create_test_folder(name="testfolder"):
    sys_tmp = tempfile.gettempdir()
    test_tmp = os.path.join(sys_tmp, name)
    if not os.path.exists(test_tmp):
        os.makedirs(test_tmp)
    tmp_dir = tempfile.mkdtemp(dir=test_tmp)
    logger.info(f"created temporary folder {tmp_dir}")
    return tmp_dir


disable_fastapi_logging()