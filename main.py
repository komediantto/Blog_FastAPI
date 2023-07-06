from fastapi import FastAPI

from app.schemas import UserCreate, UserRead

from app.manager import fastapi_users

from app.auth import auth_backend

from app.views import users_router, router as post_router

app = FastAPI(title='Simple blog')

app.include_router(post_router)
app.include_router(users_router)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
