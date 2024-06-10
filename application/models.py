from flask_login import UserMixin
from flask import current_app
from application import db
from werkzeug.security import generate_password_hash, check_password_hash
from application import login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# class Rank(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     rank_name = db.Column(db.String(20))
#     users = db.relationship('User', backref='rank', lazy='dynamic')
    
#     def __repr__(self):
#         return f'<Rank {self.rank_name}>'

class User(UserMixin, db.Model):
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    email = db.Column(db.String(120), index=True, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password_hash = db.Column(db.String(128))
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    roles = db.relationship('Role', secondary='user_roles')
    #rank_id = db.Column(db.Integer, db.ForeignKey('rank.id'))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f'<Role {self.name}>'

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
    
    def __repr__(self):
        return f'<UserRoles {self.urer_id}/ {self.role_id}>'