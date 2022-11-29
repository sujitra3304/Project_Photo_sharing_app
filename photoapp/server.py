from flask import Flask, jsonify, render_template, request, redirect, url_for, flash,session
from photoapp import app, db, bcrypt
from photoapp.forms import Registration, Login,AddComment
from photoapp.model import User, Photo, Like, Comment
from flask_login import login_user, current_user, logout_user, login_required
from photoapp import bcrypt
import photoapp.crud
import cloudinary.uploader
# import os

# CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
# CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
# CLOUD_NAME="sujitra"


# app = Flask(__name__)
# flask_bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)

# app.config['SECRET_KEY'] = '4569740e2dac685f61cbd9085d0cdb16'
# from model import db, User, Photo, Like, Comment
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    
    form = Registration()
    if form.validate_on_submit():
        username=form.username.data
        email=form.email.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # password=form.password.data
        fname=form.fname.data
        lname=form.lname.data

        user = photoapp.crud.create_user(username, email,hashed_password,fname,lname)
        db.session.add(user)
        db.session.commit()
        
        flash(f'Account created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login" , methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('homepage'))
        else:
            flash('Login Unsuccessful. Please check email and password')
    return render_template('login.html', title='Login', form=form)


@app.route('/')
def homepage():
    """Show homepage."""
    photos = Photo.query.all()
    return render_template('homepage.html', photos=photos)

@app.route('/upload')
def upload_photo():

    return render_template('upload.html')

@app.route('/show-image')
def show_image():
    """Show the saved media on a web page"""
    img_url = request.args.get('imgURL')
    return render_template('results.html', img_src=img_url)


@app.route('/post-form-data', methods=['POST'])
@login_required
def post_form_data():
    """Process form data and redirect to /show-image page"""
    my_file = request.files['my-file']
    # caption = request.form.get['caption']
    # title = request.form.get['title']
    img_url = upload_to_cloudinary(my_file)
    add_user_img_record(img_url)
    return redirect(url_for('show_image', imgURL=img_url))

def upload_to_cloudinary(media_file):
    """Upload media file to Cloudinary"""
    result = cloudinary.uploader.upload(media_file, 
                                        api_key="753998819313657", 
                                        api_secret="d8IUDEMnocqVawRUvcljkYRUpog", 
                                        cloud_name='sujitra')
    return result['secure_url']


def add_user_img_record(img_url,caption=None, title=None):
    """Stub function for persisting data to database"""
    user_id = current_user.id
    url=img_url
    photo = photoapp.crud.create_photo(user_id, url ,title,caption)
    db.session.add(photo)
    db.session.commit()
    print (current_user)
    print("\n".join([f"{'*' * 20}", "SAVE THIS url to your database!!",
                    img_url, f"{'*' * 20}" ]))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route("/account")
@login_required
def account():
    photos = Photo.query.filter_by(Photo.user.email==current_user.email).all()

    return render_template('account.html', title='Account', photos=photos)

@app.route("/photo/<int:photo_id>")
def photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    return render_template('photo.html', photo=photo)

@app.route("/add_comment/<int:photo_id>")
@login_required
def add_comment(photo_id):
    form=AddComment()
    pass




# if __name__ == '__main__':
#     # app.debug = True
#     connect_to_db(app)
#     app.run(host='0.0.0.0',debug=True)
   
