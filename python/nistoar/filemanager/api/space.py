from fastapi import APIRouter, Depends

from nistoar.filemanager.dependencies import verify_token

router = APIRouter(prefix="/oarpub")


@router.get("/fm/{name}", tags=["space"], dependencies=[Depends(verify_token)])
async def get_space_summary(name: str):
    """return a summary of space, including its current status"""
    return {"message": "Not implemented yet"}


@router.put("/fm/{name}", tags=["space"], dependencies=[Depends(verify_token)])
async def update_folder(name: str):
    """create/setup a folder with given name"""
    return {"message": "Not implemented yet"}


@router.post("/fm", tags=["space"], dependencies=[Depends(verify_token)])
async def create_folder():
    """create/setup folder; service determines/returns name."""
    return {"message": "Not implemented yet"}
