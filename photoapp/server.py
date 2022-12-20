from flask import Flask, jsonify, render_template, request, redirect, url_for, flash,session,abort
from flask_bcrypt import Bcrypt
import os
from forms import Registration, Login,AddComment
from model import User, Photo, Like, Comment, Follow, Location, db, connect_to_db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import crud
import cloudinary.uploader 


app = Flask(__name__)
app.config['SECRET_KEY'] = '4569740e2dac685f61cbd9085d0cdb16'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cloudinary"


CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUD_NAME="sujitra"
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'



@app.route("/register", methods=['GET', 'POST'])
def register():
    """Create new user"""
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    
    form = Registration()
    if form.validate_on_submit():
        username=form.username.data
        email=form.email.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        fname=form.fname.data
        lname=form.lname.data

        user = crud.create_user(username, email,hashed_password,fname,lname)
        db.session.add(user)
        db.session.commit()
        
        flash(f'Account created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login" , methods=['GET', 'POST'])
def login():
    """handle user login"""

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
@login_required
def homepage():
    """Show homepage."""
    photos = Photo.query.all()
    for photo in photos:
        print(f'HOMEPAGE PHOTO.LIKES {photo.likes}')
    following = Follow.query.filter_by(user_id=current_user.id).all()     
    following_list = []
    likes = Like.query.filter_by(user_id=current_user.id).all()
    current_user_likes=[]
    print (f' HOMEPAGE LIKES {likes}')
    all_photos = []
    recommended_follows=[]
    print(f'CURREnT USER {current_user}')
    for follow in following:
        following_list.append(follow.following_user_id)
        all_photos.extend(Photo.query.filter_by(user_id=follow.following_user_id).all())
    all_photos.extend(Photo.query.filter_by(user_id=current_user.id).all())
    
    for recommended in photos:
        
        if recommended not in recommended_follows and recommended.user_id != current_user.id and recommended.user_id not in following_list:
             recommended_follows.extend(Photo.query.filter_by(user_id=recommended.user_id).all())

    for like in likes:
        current_user_likes.append(like.photo_id)
    print(f'CURRENT USER LIKES {current_user_likes}')
    
    print(f'HOME ROUTE FOLLOWING LIST {following_list}')    
    
    return render_template('homepage.html', photos=photos, following = following,
                            all_photos=all_photos, recommended_follows=recommended_follows, current_user_likes=current_user_likes)
    
    

@login_manager.user_loader
def load_user(id):

    return User.query.get(id)


@app.route('/upload_profile_pic')
def upload_profile_pic():
    return render_template('profile_photo_upld.html')

@app.route('/upload')
@login_required
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
    img_url = upload_to_cloudinary(my_file)
    add_user_img_record(img_url)
    return redirect(url_for('show_image', imgURL=img_url))

@app.route('/profile_photo_upld', methods=['POST'])
@login_required
def profile_photo_upld():
    """Process form data and redirect to /show-image page"""
    my_file = request.files['my-file']
    img_url = upload_to_cloudinary(my_file)
    add_profile_pic(img_url)
    return redirect(url_for('show_image', imgURL=img_url))


def upload_to_cloudinary(media_file):
    """Upload media file to Cloudinary"""
    result = cloudinary.uploader.upload(media_file, 
                                        api_key="753998819313657", 
                                        api_secret="d8IUDEMnocqVawRUvcljkYRUpog", 
                                        cloud_name='sujitra')
    return result['secure_url']

def add_profile_pic(img_url):
    """add profile pic to databas"""
    profile_pic = User.query.get(current_user.id)
    profile_pic.profile_pic_url = img_url
    db.session.commit()
    print (profile_pic.profile_pic_url)
    

def add_user_img_record(img_url,caption=None, title=None):
    """add photo to database"""
    user_id = current_user.id
    url=img_url
    print(f'URL {url}')
    photo = crud.create_photo(user_id, url ,title,caption)
    db.session.add(photo)
    db.session.commit()
   


@app.route("/logout")
def logout():
    """loging out user"""
    logout_user()
    return redirect(url_for('homepage'))

@app.route("/account/<user_id>")
@login_required
def account(user_id):
    """displays username and photos that were posted by this user""" 
    user_id=(int(user_id))
    user = User.query.get(user_id)
    
    photos= Photo.query.filter(Photo.user_id==user_id).all()
    if current_user.is_authenticated:
        return render_template('account.html', title='Account', photos=photos,user=user)
    else:
         return redirect(url_for('login'))

@app.route("/photo/<int:photo_id>")
def photo(photo_id):
    """show selected photo, likes, and comments for this particular photo id"""
    photo_id = (int(photo_id))
    if current_user.is_authenticated:
        photo = Photo.query.get_or_404(photo_id)
        comments = Comment.query.filter(Comment.photo_id==photo_id).all()
        likes = Like.query.filter(Like.user_id==current_user.id, Like.photo_id==photo_id).first()
        following = Follow.query.filter_by(user_id=current_user.id, following_user_id=photo.user_id).all()
        location = Location.query.filter_by(photo_id=photo_id).first()
        form=AddComment()
        if not location:
            location = False

        print(f'************PHOTO ROUTE LOC {location}')
        print(likes)
        # print(f'PHOTO ROUTE FOLLOWING{following}')
        # print(likes)
        # print(current_user)
        
        return render_template('photo.html', photo=photo, form=form,comments=comments,likes=likes, current_user=current_user,following=following, location=location)
    
    else:
        return redirect(url_for('login'))


@app.route("/add_comment/<int:photo_id>", methods=['GET','POST'])
@login_required
def add_comment(photo_id):
    form=AddComment()
    if form.validate_on_submit():
        
        photo = Photo.query.get_or_404(photo_id)
        comment = form.comment.data
        user_id=current_user.id
        photo_id = photo_id
        next_page = request.args.get('next')
        new_comment = crud.create_comment(comment,user_id, photo_id)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(next_page) if next_page else redirect(url_for('photo',photo_id=photo_id))
    return render_template('photo.html', title='Photo',form=form,photo=photo,photo_id=photo_id)
    
   
@app.route("/like/<photo_id>", methods=['GET','POST'])
@login_required
def like(photo_id):
    """To toggle the like button and update Like table if user has like or unlike the photo"""

    photo_id=int(photo_id)
    print(type(photo_id))
    print (f'************{photo_id}')
    
    photo = Photo.query.filter_by(id=photo_id).first()
    like = Like.query.filter_by(user_id=current_user.id, photo_id=photo_id).first()
    liked = None
    if not photo:
        return jsonify({'error': 'Photo does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
        liked = "False"
    else:
        like = Like(user_id=current_user.id, photo_id=photo_id)
        db.session.add(like)
        db.session.commit()
        liked = "True"
    print (like)
    print (liked)
    return jsonify({"likes": len(photo.likes), "liked": liked})

@app.route("/delete_photo/<photo_id>", methods=['POST'])
@login_required
def delete_photo(photo_id):
    photo_id=int(photo_id)
    photo = Photo.query.get_or_404(photo_id)
    comments = Comment.query.filter(photo_id==photo_id).all()
    likes = Like.query.filter(photo_id==photo_id).all()
    locations = Location.query.filter(photo_id==photo_id).all()
    print(f'########{photo}')
    if photo.user.id != current_user.id:
         abort(403)
    
    db.session.delete(photo)
    for comment in comments:
        db.session.delete(comment)
    for like in likes:
        db.session.delete(like)
    for location in locations:
        db.session.delete(location)

    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('homepage'))

@app.route("/delete_comment/<comment_id>", methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment_id = int(comment_id)
    comment = Comment.query.get_or_404(comment_id)
    
    
    if comment.user.id != current_user.id:
         abort(403)
    
    db.session.delete(comment)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('homepage'))

@app.route("/follow/<following_user_id>", methods=['POST'])
@login_required
def follow_user(following_user_id):
    # print(f'FOLLOWING USER ID {following_user_id}')
    follow = Follow.query.filter_by(following_user_id=following_user_id).first()
    followed = None

    if not follow:
        follow = Follow(user_id=current_user.id,following_user_id=following_user_id)
        db.session.add(follow)
        db.session.commit()
        followed = True
    else:
        db.session.delete(follow)
        db.session.commit()
        followed = False

    print(f'FOLLOWED {followed} TYPE(type({followed}))')
    return jsonify({"followed": followed})

@app.route("/location/<photo_id>", methods=['POST','GET'])
@login_required
def location(photo_id):
    print (f'PHOTO LOCATION ROUTE{photo_id}')
    photo_id=(int(photo_id))
    photo = Photo.query.get_or_404(photo_id)
    location = Location.query.filter_by(photo_id=photo_id).first()
    print (photo_id)
    print (f'LOCATION QUERY {location}')
    
    if not location and photo.user_id == current_user.id:
        return render_template('updatelocation.html')
    
    elif not location and photo.user_id != current_user.id:
        return render_template('location.html')

    elif request.method == 'GET': 
        return render_template('location.html',location=location)
    
    else:
        name = location.name
        lat=location.lat
        lng=location.lng
        photo_img = photo.url
        place_id = location.place_id
        photo_id = location.photo_id
        user_id = location.user_id
        return jsonify({'name': name, 'lat': lat, 'lng':lng, 'place_id':place_id, 'photo_id':photo_id, 'user_id':user_id, 'photo_img':photo_img})


@app.route("/update_location", methods=["POST","GET"]) 
@login_required
def update_location():
    address = request.args.get('address')
    photo_id = request.args.get('photoId')
    name = request.args.get('name')
    place_id = request.args.get('place-id')
    lat = request.args.get('lat')
    lat = (float(lat))
    lng = request.args.get('lng')
    lng = (float(lng))
    user_id = current_user.id 
    # photo = Photo.query.get_or_404(photo_id)
    photo_location = Location(name=name, place_id=place_id,lat=(float(lat)),lng=(float(lng)), user_id=(int(user_id)), photo_id=(int(photo_id)))

    db.session.add(photo_location)
    db.session.commit()

    print(f'PHOTOID {photo_id}')
    print (f'ADDRESS {address}')
    return redirect(url_for('location', photo_id=photo_id))

@app.route("/to_location/<photo_id>")
@login_required 
def to_location_page(photo_id):
    photo = Photo.query.get(photo_id)
    

    # return  render_template('updatelocation.html', photo=photo)
    return redirect(url_for('location',photo_id=photo_id))

@app.route("/account_map/<user_id>", methods=["POST"])
@login_required
def map_on_account(user_id):
    locations = Location.query.filter_by(user_id=user_id).all()
    location_dict ={}

    for location in locations:
        location_dict[location.id] = {'name':location.name, 'lat':location.lat, 'lng':location.lng, 'photo_id':location.photo_id, 'user_id':location.user_id, 'imgurl':location.photo.url}
    # print (f'************{location_dict}')
    return jsonify(location_dict)


if __name__ == '__main__':
    app.debug = True
    connect_to_db(app)
    app.run(host='0.0.0.0',debug=True)
   
 




