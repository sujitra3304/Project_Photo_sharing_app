"""CRUD for Cloudinary"""

from model import db, User, Photo, Like, Comment, connect_to_db

def create_user(email, password, fname, lname):
    """Create and return a new user."""

    user = User(email=email, password=password, fname=fname,lname=lname)

    return user

def create_photo(url):
    """Create photo"""
    photo = Photo(url=url)

    return photo

def create_like(photo_id):
    """Create Like"""
    like = Like(photo_id=photo_id)

    return like

def create_comment(comment,user_id,photo_id):
    """Create Comment"""
    comment = Comment(comment=comment, user_id=user_id,photo_id=photo_id)

    return comment