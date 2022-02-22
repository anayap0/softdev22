from datetime import datetime
from hashlib import md5
from time import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import app, db, login


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    # __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    # __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    body = db.Column(db.String(140))
    image_url = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Tag relationships
    post_course_group_tags = db.relationship('CourseGroupTag', backref='post', lazy='dynamic')
    post_course_tags = db.relationship('CourseTag', backref='post', lazy='dynamic')
    post_unit_tags = db.relationship('UnitTag', backref='post', lazy='dynamic')
    post_subunit_tags = db.relationship('SubUnitTag', backref='post', lazy='dynamic')
    post_school_tags = db.relationship('SchoolTag', backref='post', lazy='dynamic')
    post_subject_tags = db.relationship('SubjectTag', backref='post', lazy='dynamic')
    post_topic_tags = db.relationship('TopicTag', backref='post', lazy='dynamic')

    def __repr__(self):
        return f'<Post: {self.title}\n{self.body}>'

# Tag Models
class CourseGroupTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    course_group_id = db.Column(db.Integer, db.ForeignKey('course_group.id'))

class SchoolTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))

class CourseTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

class UnitTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))

class SubUnitTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    subunit_id = db.Column(db.Integer, db.ForeignKey('subunit.id'))

class SubjectTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))

class TopicTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))

class CourseGroup(db.Model):
    __tablename__ = 'course_group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True, index=True)
    courses = db.relationship('Course', backref='group', lazy='dynamic')
    tags = db.relationship('CourseGroupTag', backref='group', lazy='dynamic')

class School(db.Model):
    # __tablename__ = 'school'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    tags = db.relationship('SchoolTag', backref='school', lazy='dynamic')

class Course(db.Model):
    # __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(28))
    course_group_id = db.Column(db.Integer, db.ForeignKey('course_group.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id')) 
    units = db.relationship('Unit', backref='corr_course', lazy='dynamic') # corr_course = corresponding course
    tags = db.relationship('CourseTag', backref='course', lazy='dynamic')

class Unit(db.Model):
    # __tablename__ = 'unit'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    name = db.Column(db.String)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    subunits = db.relationship('SubUnit', backref='corr_unit', lazy='dynamic') # corr_unit = corresponding unit
    tags = db.relationship('UnitTag', backref='unit', lazy='dynamic')

class SubUnit(db.Model):
    __tablename__ = 'subunit'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))
    tags = db.relationship('SubUnitTag', backref='subunit', lazy='dynamic')

# For more generic subjects than Course (e.g., biology as opposed to AP Biology)
class Subject(db.Model):
    # __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    topics = db.relationship('Topic', backref='corr_subject', lazy='dynamic') # corr_subject = corresponding subject
    tags = db.relationship('SubjectTag', backref='subject', lazy='dynamic')

class Topic(db.Model):
    # __tablename__ = 'topic'
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    tags = db.relationship('TopicTag', backref='topic', lazy='dynamic')