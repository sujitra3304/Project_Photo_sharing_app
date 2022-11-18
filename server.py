from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from forms import Registration, Login
from model import connect_to_db, db, User, Photo, Like, Comment
import crud
import cloudinary.uploader
import os

CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUD_NAME="sujitra"


app = Flask(__name__)
app.config['SECRET_KEY'] = '4569740e2dac685f61cbd9085d0cdb16'
# from model import db, User, Photo, Like, Comment
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = Registration()
    if form.validate_on_submit():
        # user = User(email=form.email.data,password=form.password.data,fname=form.fname.data, lname=form.lname.data)
        # db.session.add(user)
        # db.session.commit()
        email=form.email.data
        password=form.password.data
        fname=form.fname.data
        lname=form.lname.data

        user = crud.create_user(email,password,fname,lname)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login" , methods=['GET', 'POST'])
def login():
    form = Login()
    return render_template('login.html', title='Login', form=form)


@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')

@app.route('/upload')
def upload_photo():

    return render_template('upload.html')

@app.route('/show-image')
def show_image():
    """Show the saved media on a web page"""
    img_url = request.args.get('imgURL')
    return render_template('results.html', img_src=img_url)


@app.route('/post-form-data', methods=['POST'])
def post_form_data():
    """Process form data and redirect to /show-image page"""
    my_file = request.files['my-file']
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


def add_user_img_record(img_url):
    """Stub function for persisting data to database"""
    print("\n".join([f"{'*' * 20}", "SAVE THIS url to your database!!",
                    img_url, f"{'*' * 20}" ]))



if __name__ == '__main__':
    # app.debug = True
    connect_to_db(app)
    app.run(host='0.0.0.0',debug=True)
   
