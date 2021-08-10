from fastapi import FastAPI, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

api = FastAPI()
security = HTTPBasic()


users = {"daniel": "1234", "john.doe": "pwd"}


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username not in users:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    password = users[credentials.username]

    if password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username


@api.get("/")
async def root(credentials: HTTPBasicCredentials = Depends(get_current_username)):
    return {"message": "Hello World"}
