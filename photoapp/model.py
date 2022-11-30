"""Models for movie ratings app."""



from datetime import datetime
from photoapp import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class User(db.Model, UserMixin):
    """A user."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True,
                        nullable = False)
    username = db.Column(db.String(20),
                          unique=True,
                          nullable = False  )
    email = db.Column(db.String(30), 
                      unique= True,
                      nullable=False)
    password = db.Column(db.String(100),
                         nullable=False)
    fname = db.Column(db.String(20),
                      nullable=False)
    lname = db.Column(db.String(20),
                      nullable=False)

    photo=db.relationship("Photo", back_populates="user")
    comment=db.relationship("Comment", back_populates="user")
    like=db.relationship("Like", back_populates="user")
    
    def __repr__(self):
        return f'<User user_id={self.id} username={self.username} email={self.email} first_name={self.fname} last_name={self.lname}>'

class Photo(db.Model):
    """photos"""
    __tablename__ = "photos"
    id = db.Column(db.Integer,
                        autoincrement = True,
                        primary_key=True,
                        nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    title = db.Column(db.String)
    caption = db.Column(db.String)
    url = db.Column(db.String,
                    nullable=False)      
    date = db.Column(db.Date, 
                    default=datetime.utcnow)

    user=db.relationship("User", back_populates="photo")

    def __repr__(self):
        return f'<Photo photo_id={self.id} url={self.url} caption={self.caption} title={self.title} user_id={self.user_id} date={self.date} username={self.user.username}>'


class Like(db.Model):
    __tablename__ = "likes"
    id = db.Column(db.Integer,
                    autoincrement=True,
                    primary_key=True)
    photo_id = db.Column(db.Integer, 
                        db.ForeignKey("photos.id"))
    user_id = db.Column(db.Integer,
                         db.ForeignKey("users.id"))
    like_date = db.Column(db.Date, default=datetime.utcnow)
    user=db.relationship("User", back_populates="like")

    def __repr__(self):
        return f'<Like photo_id = {self.photo_id}, user_id={self.user_id}, like_date={self.like_date}>'


class Comment(db.Model):
    __tablename__ = "comments"
    
    id = db.Column(db.Integer,
                   autoincrement = True,
                   primary_key=True,
                   nullable=False)
    photo_id = db.Column(db.Integer, 
                         db.ForeignKey("photos.id"))
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"))
    comment = db.Column(db.String(300), 
                        nullable = False)
    comment_date = db.Column(db.Date, default=datetime.utcnow)
    user = db.relationship("User", back_populates="comment")

    def __repr__(self):
        return f'<Comment comment_id = {self.id} photo_id={self.photo_id}, user_id={self.user_id}, comment={self.comment}, comment_date={self.comment_date}>'

class Follow(db.Model):
    __tablename__ ="followers"
    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True) 
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"))
    following_user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"))


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
