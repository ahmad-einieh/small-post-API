import imp


import datetime
import sqlalchemy as _sqlalchemy
import sqlalchemy.orm as _orm
#import _sqlalchemy.ext.declarative as dec
import passlib.hash as hash

import database

class userModel(database.Base):
    __tablename__ = "users"
    id = _sqlalchemy.Column(_sqlalchemy.Integer, primary_key=True, index=True)
    email = _sqlalchemy.Column(_sqlalchemy.String, unique=True, index=True)
    name = _sqlalchemy.Column(_sqlalchemy.String)
    phone = _sqlalchemy.Column(_sqlalchemy.String)
    password_hash = _sqlalchemy.Column(_sqlalchemy.String)
    created_At = _sqlalchemy.Column(_sqlalchemy.DateTime, default=datetime.datetime.utcnow())
    posts = _orm.relationship("postModel", back_populates="owner")

    def password_verification(self,password:str):
        return hash.bcrypt.verify(password,self.password_hash)



class postModel(database.Base):
    __tablename__ = "posts"
    id = _sqlalchemy.Column(_sqlalchemy.Integer, primary_key=True, index=True)
    user_id = _sqlalchemy.Column(_sqlalchemy.Integer, _sqlalchemy.ForeignKey("users.id"))
    title = _sqlalchemy.Column(_sqlalchemy.String)
    content = _sqlalchemy.Column(_sqlalchemy.String)
    image = _sqlalchemy.Column(_sqlalchemy.String)
    created_At = _sqlalchemy.Column(_sqlalchemy.DateTime, default=datetime.datetime.utcnow())
    user = _orm.relationship("userModel", back_populates="posts")


