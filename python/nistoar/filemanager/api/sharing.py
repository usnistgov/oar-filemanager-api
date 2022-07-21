from fastapi import APIRouter, Depends

from nistoar.filemanager.dependencies import verify_token

router = APIRouter(prefix="/oarpub")


@router.get("/fm/{name}/acls", tags=["sharing"], dependencies=[Depends(verify_token)])
async def list_permissions(name: str):
    """return a summary of currently set permissions."""
    return {"message": "Not implemented yet"}


@router.patch("/fm/{name}/acls", tags=["sharing"], dependencies=[Depends(verify_token)])
async def edit_permissions(name: str):
    """change permissions."""
    return {"message": "Not implemented yet"}

