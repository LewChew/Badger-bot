from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from passlib.hash import sha256_crypt

from badger_bot import app, mysql
from badger_bot.models import User, Post
from badger_bot.forms import PostForm

from twilio.twiml.messaging_response import MessagingResponse, Message
from twilio.rest import Client

import os
import urllib

# Account SID and Auth Token from www.twilio.com/console
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

@app.route("/")
def index():
    mysql.create_all()
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


@app.route("/about")
def about():
    return render_template("index.html")


@app.route("/register", methods=['GET', 'POST'])
def register():

    if request.method == 'GET':
        return render_template('register.html')

    else:
        # Create user object to insert into SQL
        passwd1 = request.form.get('password1')
        passwd2 = request.form.get('password2')

        if passwd1 != passwd2 or passwd1 == None:
            flash('Password Error!', 'danger')
            return render_template('register.html')

        hashed_pass = sha256_crypt.encrypt(str(passwd1))

        new_user = User(
            username=request.form.get('username'),
            email=request.form.get('username'),
            password=hashed_pass)

        if user_exsists(new_user.username, new_user.email):
            flash('User already exsists!', 'danger')
            return render_template('register.html')
        else:
            # Insert new user into SQL
            mysql.session.add(new_user)
            mysql.session.commit()

            login_user(new_user)

            flash('Account created!', 'success')
            return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    else:
        username = request.form.get('username')
        password_candidate = request.form.get('password')

        # Query for a user with the provided username
        result = User.query.filter_by(username=username).first()

        # If a user exsists and passwords match - login
        if result is not None and sha256_crypt.verify(password_candidate, result.password):

            # Init session vars
            login_user(result)
            flash('Logged in!', 'success')
            return redirect(url_for('index'))

        else:
            flash('Incorrect Login!', 'danger')
            return render_template('login.html')


@app.route("/logout")
def logout():
    logout_user()
    flash('Logged out!', 'success')
    return redirect(url_for('index'))


# Check if username or email are already taken
def user_exsists(username, email):
    # Get all Users in SQL
    users = User.query.all()
    for user in users:
        if username == user.username or email == user.email:
            return True

    # No matching user
    return False

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        mysql.session.add(post)
        mysql.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        mysql.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    mysql.session.delete(post)
    mysql.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('index'))

@app.route("/startBadger")
def outbound_sms():
    args = request.args
    phoneTo = args.get("phone")
    if phoneTo:
        message = client.messages \
            .create(
            body='You have released the Badger! Are you ready?',
            from_='2602701024',
            to= phoneTo
        )
        flash('Check your phone for the Badger', 'success')
        return render_template('released.html')
    else:
        message2 = "add phone Parameters to request"
        return message2

@app.route('/call', methods=['POST'])
def outbound_call():
    song_title = request.args.get('track')
    track_url = 'Testing123'

    response = MessagingResponse()
    response.play(track_url)
    return str(response)

@app.route('/sms', methods=['POST'])
def inbound_sms():
    response = MessagingResponse()
    response.message('Everybody needs a badger!')

    # Grab the song title from the body of the text message.
    # song_title = urllib.parse.quote(request.form['Body'])
    
    #print(song_title)
    # Grab the relevant phone numbers.
    from_number = request.form['From']
    to_number = request.form['To']
    twiml_1 = '<Response><Say>Hello, You have released the badger. Proceed with caution.</Say></Response>'
    # Create a phone call that uses our other route to play a song from Spotify.
    client.api.account.calls.create(to=from_number, from_=to_number, twiml=twiml_1)

   # client.api.account.calls.create(to=from_number, from_=to_number,
   #                    url='http://2b66-71-184-198-93.ngrok.io/call?track={}'
   #                     .format(song_title))

    return str(response)
