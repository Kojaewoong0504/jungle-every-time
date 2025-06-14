from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, func
from src.app.core.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email: str = Column(String(255), unique=True, nullable=False)
    username = Column(String(255), nullable=False)
    password = Column(Text, nullable=False)
    nickname = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    # 관계 매핑
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    post_likes = relationship("PostLike", back_populates="user")


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    likes = Column(Integer, nullable=False, default=0)
    views = Column(Integer, nullable=False, default=0)
    user_id = Column(Integer, ForeignKey('users.id'))
    board_id = Column(Integer, ForeignKey('boards.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="posts")
    board = relationship("Board", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    post_likes = relationship("PostLike", back_populates="post")


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    comment = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    posts_id = Column(Integer, ForeignKey('posts.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")


class PostLike(Base):
    __tablename__ = 'post_likes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Boolean, nullable=False, default=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    posts_id = Column(Integer, ForeignKey('posts.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="post_likes")
    post = relationship("Post", back_populates="post_likes")


class Board(Base):
    __tablename__ = 'boards'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    topic = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    posts = relationship("Post", back_populates="board")
