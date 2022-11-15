"""Models for movie ratings app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()



class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True,
                        nullable = False)
    email = db.Column(db.String(30), 
                      unique= True,
                      nullable=False)
    password = db.Column(db.String(20),
                         nullable=False)
    fname = db.Column(db.String(20),
                      nullable=False)
    lname = db.Column(db.String(20),
                      nullable=False)

    photo=db.relationship("Photo", back_populates="user")
    
    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email} first_name={self.fname} last_name={self.lname}>'

class Photo(db.Model):
    """photos"""
    __tablename__ = "photos"
    photo_id = db.Column(db.Integer,
                        autoincrement = True,
                        primary_key=True,
                        nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey("users.user_id"))
    caption = db.Column(db.String)
    url = db.Column(db.String,
                    nullable=False)      
    date = db.Column(db.Date, 
                    default=datetime.utcnow)

    user=db.relationship("User", back_populates="photo")

    def __repr__(self):
        return f'<Photo url={self.url} caption={self.caption} user_id={self.user_id} date={self.date}>'


class Like(db.Model):
    __tablename__ = "likes"
    id = db.Column(db.Integer,
                    autoincrement=True,
                    primary_key=True)
    photo_id = db.Column(db.Integer, 
                        db.ForeignKey("photos.photo_id"))
    user_id = db.Column(db.Integer,
                         db.ForeignKey("users.user_id"))
    like_date = db.Column(db.Date, default=datetime.utcnow)

    def __repr__(self):
        return f'<Like photo_id = {self.photo_id}, user_id={self.user_id}, like_date={self.like_date}>'


class Comment(db.Model):
    __tablename__ = "comments"
    
    id = db.Column(db.Integer,
                   autoincrement = True,
                   primary_key=True,
                   nullable=False)
    photo_id = db.Column(db.Integer, 
                         db.ForeignKey("photos.photo_id"))
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"))
    comment = db.Column(db.String(300), 
                        nullable = False)
    comment_date = db.Column(db.Date, default=datetime.utcnow)

    def __repr__(self):
        return f'<Comment photo_id={self.photo_id}, user_id={self.user_id}, comment={self.comment}, comment_date={self.comment_date}>'

        
def connect_to_db(flask_app, db_uri="postgresql:///cloudinary", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
