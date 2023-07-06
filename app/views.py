from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .db import get_async_session
from .models import Mark, Post, User
from .manager import current_user
from .schemas import PostCreate
from . import constants

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

users_router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/')
async def create_post(new_post: PostCreate,
                      user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    async with session:
        post = Post(text=new_post.text, author_id=user.id)
        session.add(post)
        await session.commit()
        await session.refresh(post)
    return {"message": constants.POST_CREATED.format(email=user.email)}


@router.get('/')
async def posts_list(session: AsyncSession = Depends(get_async_session),
                     user: User = Depends(current_user)):
    query = select(Post)
    posts = await session.execute(query)
    return posts.scalars().all()


@router.delete('/{id}')
async def post_delete(id: int,
                      user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    query = select(Post).where(Post.id == id)
    result = await session.execute(query)
    post = result.scalars().first()
    if post is not None:
        if post.author_id != user.id:
            raise HTTPException(status_code=403,
                                detail=constants.CANNOT_DELETE)
        else:
            await session.delete(post)
            await session.commit()
            return {"message": constants.POST_DELETED.format(id=id)}
    else:
        raise HTTPException(status_code=404,
                            detail=constants.POST_NOT_FOUND)


@router.patch('/{id}')
async def post_update(id: int,
                      text: str,
                      user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    query = select(Post).where(Post.id == id)
    result = await session.execute(query)
    post = result.scalars().first()
    if post is not None:
        if post.author_id != user.id:
            raise HTTPException(status_code=403,
                                detail=constants.CANNOT_UPDATE)
        else:
            post.text = text
            await session.commit()
            return {"message": constants.POST_UPDATED.format(id=id)}
    else:
        raise HTTPException(status_code=404,
                            detail=constants.POST_NOT_FOUND)


@router.get('/me')
async def my_posts_list(session: AsyncSession = Depends(get_async_session),
                        user: User = Depends(current_user)):
    query = select(Post).where(Post.author_id == user.id)
    posts = await session.execute(query)
    return posts.scalars().all()


@users_router.get('/{email}/posts')
async def user_posts_list(email: EmailStr,
                          session: AsyncSession = Depends(get_async_session)):
    user_query = select(User).where(User.email == email)
    user_result = await session.execute(user_query)
    user = user_result.scalar()

    posts_query = select(Post).where(Post.author_id == user.id)
    posts_result = await session.execute(posts_query)
    posts = posts_result.scalars().all()

    return posts


@router.post('/{id}/like')
async def post_like(id: int,
                    user: User = Depends(current_user),
                    session: AsyncSession = Depends(get_async_session)):
    query = select(Post).where(Post.id == id)
    result = await session.execute(query)
    post = result.scalars().first()

    if post is not None:
        if post.author_id == user.id:
            raise HTTPException(
                status_code=403,
                detail=constants.CANNOT_ESTIMATE)
        else:
            query = select(Mark).filter(
                Mark.user_id == user.id, Mark.post_id == post.id)
            result = await session.execute(query)
            mark = result.scalars().first()
            if mark is not None:
                if mark.value:
                    return {"message": constants.ALREADY_LIKE.format(id=id)}
                elif not mark.value:
                    mark.value = True
                    await session.commit()
                    return {"message": constants.NOW_YOU_LIKE.format(id=id)}
            else:
                mark = Mark(user_id=user.id, post_id=post.id, value=True)
                session.add(mark)
                await session.commit()
                await session.refresh(mark)
                return {"message": constants.LIKE.format(id=id)}
    else:
        raise HTTPException(status_code=404,
                            detail=constants.POST_NOT_FOUND)


@router.post('/{id}/dislike')
async def post_dislike(id: int,
                       user: User = Depends(current_user),
                       session: AsyncSession = Depends(get_async_session)):
    query = select(Post).where(Post.id == id)
    result = await session.execute(query)
    post = result.scalars().first()
    if post is not None:
        if post.author_id == user.id:
            raise HTTPException(
                status_code=403,
                detail=constants.CANNOT_ESTIMATE)
        else:
            query = select(Mark).filter(
                Mark.user_id == user.id, Mark.post_id == post.id)
            result = await session.execute(query)
            mark = result.scalars().first()
            if mark is not None:
                if not mark.value:
                    return {"message": constants.ALREADY_DISLIKE.format(id=id)}
                elif mark.value:
                    mark.value = False
                    await session.commit()
                    return {"message": constants.NOW_YOU_DISLIKE.format(id=id)}
            else:
                mark = Mark(user_id=user.id, post_id=post.id, value=False)
                session.add(mark)
                await session.commit()
                await session.refresh(mark)
                return {"message": constants.DISLIKE.format(id=id)}
    else:
        raise HTTPException(status_code=404,
                            detail=constants.POST_NOT_FOUND)
