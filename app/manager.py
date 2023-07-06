import uuid
from typing import Optional

from fastapi import Depends, HTTPException, Request
from fastapi_users import (BaseUserManager, FastAPIUsers,
                           UUIDIDMixin, schemas, models)
from loguru import logger


from .db import User, get_user_db
import config as cfg
from .auth import auth_backend
import requests
from .constants import EMAIL_VERIFY, EMAIL_DOES_NOT_EXIST, HUNTER_NOT_AVAILABLE

SECRET = cfg.USER_SECRET_KEY


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        if self.verify_email(user_create.email, cfg.EMAIL_API):
            user = await super().create(user_create, safe, request)
            return user
        else:
            raise HTTPException(status_code=403,
                                detail=EMAIL_DOES_NOT_EXIST.format(
                                    email=user_create.email))

    def verify_email(self, email: str, api_key: str) -> bool:
        url = EMAIL_VERIFY.format(email=email, api_key=api_key)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data["data"]["status"] != "invalid":
                return True
        elif response.status_code != 200:
            raise HTTPException(status_code=404,
                                detail=HUNTER_NOT_AVAILABLE)
        else:
            return False

    async def on_after_register(self, user: User,
                                request: Optional[Request] = None):
        logger.info(f"User {user.id} has registered.")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
