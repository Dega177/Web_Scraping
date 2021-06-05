from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import models


class Database:

    def __init__(self, db_url):
        engine = create_engine(db_url)
        models.Base.metadata.create_all(bind=engine)
        self.maker = sessionmaker(bind=engine)

    def get_or_create(self, session, model, filter_field, data):
        instance = session.query(model).filter_by(**{filter_field: data[filter_field]}).first()
        if not instance:
            instance = model(**data)
        return instance

    def add_post(self, data):
        session = self.maker()
        post = self.get_or_create(session, models.Post, 'id', data['post_data'])
        author = self.get_or_create(session, models.Author, 'url', data['author_data'])
        post.author = author
        if data['comments_data']:
            for item in data['comments_data']:
                comment = {k: v for k, v in item.items() if k != 'full_name'}
                user = {k: v for k, v in item.items() if k in ['user_id', 'full_name']}
                comment = self.get_or_create(session, models.Comment, 'id', comment)
                user = self.get_or_create(session, models.User, 'user_id', user)
                comment.post = post
                comment.user = user
                session.add(comment)
        for tag in data['tags_data']:
            tag = self.get_or_create(session, models.Tag, 'url', tag)
            tag.post.append(post)
            session.add(tag)
        session.add(post)
        try:
            session.commit()
        except Exception:
            session.rollback()
        finally:
            session.close()
