import logging
import os
import sys
import tempfile
from loguru import logger
from loguru._defaults import LOGURU_FORMAT


def disable_uvicorn_logging():
    uvicorn_error = logging.getLogger("uvicorn.error")
    uvicorn_error.disabled = True
    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_access.disabled = True


NONE_LOG_LEVEL = "NONE"
DEFAULT_LOG_LEVEL = "DEBUG"

LONG_FORMAT = LOGURU_FORMAT
SHORT_FORMAT = "<yellow>{time:YYYY-MM-DD at HH:mm:ss}</yellow> | <level>[{level}]</level> {message}"

def initialize_logger(name, log_level=DEFAULT_LOG_LEVEL):
    """Initiialize Logaru logger."""

    logger.remove()

    if log_level == NONE_LOG_LEVEL:
        logger.disable(name)
        return

    if log_level == "DEBUG":
        log_format = LONG_FORMAT
    else:
        log_format = SHORT_FORMAT

    logger.add(sys.stdout, colorize=True, format=log_format, level=log_level)
    logger.enable(name)


def create_test_folder(name="testfolder"):
    """Create a temporary folder for testing purposes."""

    sys_tmp = tempfile.gettempdir()
    test_tmp = os.path.join(sys_tmp, name)
    if not os.path.exists(test_tmp):
        os.makedirs(test_tmp)
    tmp_dir = tempfile.mkdtemp(dir=test_tmp)
    logger.debug(f"created temporary folder {tmp_dir}")
    return tmp_dir

def build_url(host, port, endpoint="", scheme="http"):
    """Build url."""

    url = f"{scheme}://{host}"
    if port is not None:
        url += f":{port}"
    url += f"/{endpoint}"
    return url 

disable_uvicorn_logging()
