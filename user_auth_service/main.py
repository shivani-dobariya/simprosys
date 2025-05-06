import os

import bcrypt
import uvicorn
from dotenv import load_dotenv
from fastapi import Depends
from fastapi import FastAPI
from fastapi import status
from sqlalchemy import select
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from auth import decode_jwt
from models import get_session
from models.db_models import User
from models.schema_models import UserCreate, UserID

load_dotenv()

salt = os.getenv('salt')
JWT_SECRET = os.getenv('JWT_SECRET')
auth_expire_time = os.getenv('auth_expire_time')
refresh_expire_time = os.getenv('refresh_expire_time')

app = FastAPI()


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        # do something with the request object
        content_type = request.headers.get('Content-Type')
        print(content_type)
        token = ''
        if decode_jwt(token=token):
            # process the request and get the response
            return await call_next(request)

    # async def __call__(self, request: Request, call_next, response: Response):
    # # do something with the request object
    # content_type = request.headers.get('Content-Type')
    # print(content_type)
    # token = ''
    # if decode_jwt(token=token):
    #     # process the request and get the response
    #     response = await call_next(request)
    # else:
    #     response.status_code = status.HTTP_401_UNAUTHORIZED
    #
    # return response


app.add_middleware(AuthMiddleware)


@app.post("/create-user/")
async def create_user(data: UserCreate, response: Response, db_session=Depends(get_session)):
    try:
        async with db_session as session:
            db_obj = User(name=data.name, email=data.email, password=bcrypt.hashpw(data.password, salt))
            session.add(db_obj)
            session.commit()
        return {"data": db_obj, "status": True, "message": "user created"}

    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return {"data": {}, "status": False, "message": "error while creating user"}


@app.post("/user-detail/")
async def get_user(data: UserID, response: Response, db_session=Depends(get_session)):
    try:
        async with db_session as session:
            existing_user = (
                await session.scalars(select(User).where(User.id == data.id, User.is_deleted == False))).first()
        if existing_user:
            return {"data": existing_user or {}, "status": True, "message": "user fetched"}
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"data": {}, "status": True, "message": "no user found"}

    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return {"data": [], "status": False, "message": "error while fetching user detail"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
