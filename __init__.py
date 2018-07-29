"""app db models"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.dialects.mysql import SMALLINT, TIMESTAMP, BOOLEAN
from werkzeug.security import check_password_hash

from datetime import datetime

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Interger, primary_key=True)
    username = db.Column(db.String(60), default='')
    password = db.Column(db.String(60), unique=True, default='')
    first_name = db.Column(db.String(20), default='')
    last_name = db.Column(db.String(20), default='')
    email = db.Column(db.String(60), unique=True, default='')
    join_timestamp = db.Column(TIMESTAMP, default=datetime.datetime.utcnow().replace(microsecond=0))
    is_admin = db.Column(BOOLEAN, default=False)

    # Class Methods
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_role(email, is_admin=False):
        role = db.session.query(
            Users
        ).filter(
            Users.email == email
        ).scalar()
        role.is_admin = is_admin
        db.session.commit()

    @staticmethod
    def get(user_id):
        user = db.session.query(
            Users
        ).filter(
            Users.user_id == user_id
        ).scalar()
        return user

    # Relationship
    posts = db.relationship('Posts', backref='post_author', passive_deletes=True, lazy='dynamic')
    newsfeed = db.relationship('Newsfeed', backref='newsfeed_author', passive_deletes=True, lazy='dynamic')


class Posts(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Interger, primary_key=True)
    title = db.Column(db.String(255), default='')
    content = db.Column(db.Text, default='')
    draft = db.Column(db.Text, default='')
    post_timestamp = db.Column(TIMESTAMP, default=datetime.datetime.utcnow().replace(microsecond=0))
    view_num = db.Column(db.Interger, default=0)

    # Class Methods
    def create_tag(self, tag_title, description, tag_type):
        new_tag = Tags(tag_title=tag_title, description=description, tag_type=tag_type)
        new_relation = Post_Tag(post_id=self.post_id, tag_id=new_tag.tag_id)
        db.session.add_all([new_tag, new_relation])
        db.session.commit()

    # Relationship
    user_id = db.Column(db.Interger, db.ForeignKey('users.user_id', ondelete="CASCADE", onupdate='CASCADE'))


class Newsfeed(db.Model):
    __tablename__ = 'newsfeed'
    newsfeed_id = db.Column(db.Interger, primary_key=True)
    title = db.Column(db.String(255), default='')
    content = db.Column(db.Text, default='')
    draft = db.Column(db.Text, default='')
    post_timestamp = db.Column(TIMESTAMP, default=datetime.datetime.utcnow().replace(microsecond=0))
    view_num = db.Column(db.Interger, default=0)
    expiry_timestamp = db.Column(TIMESTAMP)

    # Relationship
    user_id = db.Column(db.Interger, db.ForeignKey('users.user_id', ondelete="CASCADE", onupdate='CASCADE'))


class Tags(db.Model):
    __tablename__ = 'tags'
    tag_id = db.Column(db.Interger, primary_key=True)
    tag_title = db.Column(db.String(255), default='')
    description = db.Column(db.Text, default='')
    tag_type = db.Column(SMALLINT(2), default=0)


class Post_Tag(db.Model):
    __tablename__ = 'post_tag'
    post_tag_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Interger, db.ForeignKey('posts.post_id'))
    tag_id = db.Column(db.Interger, db.ForeignKey('tags.tag_id'))
