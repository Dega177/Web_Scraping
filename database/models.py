from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

Base = declarative_base()


post_to_tag = Table(
    'post_to_tag',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('post.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)


class Post(Base):

    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(2048), unique=True, nullable=False)
    title = Column(String, nullable=False, unique=False)
    first_img_url = Column(String(2048), unique=True, nullable=True)
    time = Column(DateTime, unique=False, nullable=False)
    author_id = Column(Integer, ForeignKey('author.id'), nullable=False)
    author = relationship('Author', backref='posts')
    tag = relationship('Tag', secondary=post_to_tag, back_populates='post')


class Tag(Base):

    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=True)
    url = Column(String(2048), unique=True, nullable=True)
    post = relationship('Post', secondary=post_to_tag, back_populates='tag')


class Author(Base):

    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(2048), unique=True, nullable=False)
    name = Column(String, nullable=False, unique=False)


class Comment(Base):

    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    comment = Column(String, nullable=False, unique=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    parent_id = Column(Integer, ForeignKey('comment.id'), nullable=True)
    post = relationship('Post', backref='comments')
    user = relationship('User', backref='comments')


class User(Base):

    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True, nullable=False)
    full_name = Column(String, unique=False, nullable=False)
