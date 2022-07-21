import os
from fastapi import FastAPI
from loguru import logger

from nistoar.filemanager.util import build_url, initialize_logger
from nistoar.filemanager.config import get_settings

app = FastAPI()

APP_NAME = "nistoar.filemanager.main:app"
ENV = os.environ.get("ENV", "local")

settings = get_settings(ENV)

# add logic that should be run before the application starts
@app.on_event("startup")
async def startup_event():
    logger.debug(f"Uvicorn running on: {build_url(settings.HOST,settings.PORT)}")


# add logic that should be run when the application is shutting down
@app.on_event("shutdown")
def shutdown_event():
    logger.debug(f"Uvicorn shutdown")


@app.get("/")
def read_root():
    return {"Service": "NextCloud File Manager API", "Status": "Running"}


def main():
    import uvicorn

    logger.debug(f"Using current settings: {settings.__repr__()}")

    uvicorn.run(
        app=APP_NAME,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        debug=settings.DEBUG,
    )


if __name__ == "__main__":
    initialize_logger(__name__, "DEBUG")
    main()
