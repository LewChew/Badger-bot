from datetime import datetime
from badger_bot import *
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(mysql.Model, UserMixin):
    id = mysql.Column(mysql.Integer, primary_key=True)
    username = mysql.Column(mysql.String(20), unique=True, nullable=False)
    email = mysql.Column(mysql.String(120), unique=True, nullable=False)
    password = mysql.Column(mysql.String(60), nullable=False)
    posts = mysql.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return(self.username)


class Post(mysql.Model):
    id = mysql.Column(mysql.Integer, primary_key=True)
    title = mysql.Column(mysql.String(120), nullable=False)
    date_posted = mysql.Column(mysql.DateTime, nullable=False, default=datetime.utcnow)
    content = mysql.Column(mysql.String(120), nullable=False)
    user_id = mysql.Column(mysql.Integer, mysql.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return(self.id)


