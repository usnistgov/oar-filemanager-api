from fastapi import APIRouter


router = APIRouter(prefix="/oarpub")

"""
“Status” of space and processing
    - After creation, the space is “open” for operations by user
    - When user is finished organizing, they release control of the space and let app process the contents – the space is “closed”.
    - Incremental processing: after user has added and organized a bunch of files, let app incrementally (like a “save”)
"""


# api endpoint to return status of the service and other info
@router.get("/fm/{name}/status", tags=["status"])
async def get_status(name: str):
    """get summary of status."""
    message = f"Status for space {name}"
    return {"message": message}


@router.patch("/fm/{name}/status", tags=["status"])
async def get_status():
    """update the status.

    - “save”  : trigger incremental processing of contents
    - “close” : release control of space, trigger final processing
    - “open”  : (when allowed) reopen “closed” space for further changes
    """
    return {"message": "Not implemented yet"}

