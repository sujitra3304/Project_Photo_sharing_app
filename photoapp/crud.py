"""CRUD for Cloudinary"""

from model import db, User, Photo, Like, Comment

def create_user(username, email, password, fname, lname):
    """Create and return a new user."""

    user = User(username=username,email=email, password=password, fname=fname,lname=lname)
    
    return user

def create_photo(user_id, url,caption=None,title=None):
    """Create photo"""
    photo = Photo(user_id=user_id,url=url,title=title, caption=caption)


    return photo

def create_like(photo_id):
    """Create Like"""
    like = Like(photo_id=photo_id)

    return like

def create_comment(comment,user_id,photo_id):
    """Create Comment"""
    comment = Comment(comment=comment, user_id=user_id,photo_id=photo_id)

    return comment

# if __name__ == "__main__":
#     from server import app

#     connect_to_db(app)