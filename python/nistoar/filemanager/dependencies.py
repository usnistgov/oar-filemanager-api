

from fastapi import HTTPException, Header


# an example of dependency to check token in header
async def verify_token(access_token: str = Header()):
    if access_token != "LOCAL_TOKEN":
        raise HTTPException(status_code=401, detail="Unauthorized! Access token invalid.")
