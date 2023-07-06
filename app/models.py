import datetime
import uuid

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, declarative_base, relationship

Base = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    posts = relationship('Post', back_populates='author')
    marks = relationship('Mark', back_populates='user')


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    marks = relationship('Mark', back_populates='post')
    author_id: Mapped[uuid.UUID] = Column(GUID, ForeignKey('user.id'))
    author = relationship('User', back_populates='posts')


class Mark(Base):
    __tablename__ = 'mark'

    id = Column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = Column(GUID, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    value = Column(Boolean, nullable=False)
    user = relationship('User', back_populates='marks')
    post = relationship('Post', back_populates='marks')
