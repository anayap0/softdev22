from datetime import datetime

from numpy import ALLOW_THREADS
from flask import render_template, flash, redirect, url_for, request, send_from_directory, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from app import app, db
from app.files import validate_file
from app.forms import AddCommentForm, LoginForm, RegistrationForm, EditProfileForm, \
    EmptyForm, PostForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User, Post, PostVote, Comment, School, \
    CourseGroup, Course, Unit, SubUnit, Subject, Topic, \
        CourseGroupTag, CourseTag, UnitTag, SubUnitTag, SubjectTag
from app.tags import get_tag_choices, group_classes, group_colors, write_tag_choices
from app.email import send_password_reset_email
import os


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    post = Post.query.all()
    for i in post:
        path = os.getcwd() + f"/app{i.image_url}"
        print(path)
        print(os.path.exists(path))
        if os.path.exists(path):
            os.remove(path)
        db.session.delete(i)
    db.session.commit()
    flash('deleted')
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    form.tags.choices = get_tag_choices(group_classes)
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user, title=form.title.data)
        uploaded_file = form.file.data
        if uploaded_file is not None:
            filename = secure_filename(uploaded_file.filename)
            file_ext = os.path.splitext(filename)[1]
            validated = validate_file(uploaded_file.stream)
            print("original:", file_ext)
            print("validated:", validated)
            if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                    (file_ext != validated and \
                        file_ext not in app.config['OFFICE_EXTENSIONS']):
                return "Invalid Image", 400
            db.session.add(post)
            db.session.commit()
            post_id = post.id
            tag_values=form.tags.data
            write_tag_choices(post_id, tag_values, commit=False)
            file_path = os.path.join(app.config['UPLOAD_PATH'], str(post_id) + file_ext)
            uploaded_file.save(file_path)
            post.image_url=url_for('upload', filename=str(post_id)+file_ext) # update post object with filename
            db.session.commit()
        else:
            db.session.add(post)
            db.session.commit()
            post_id = post.id
            tag_values=form.tags.data
            write_tag_choices(post_id, tag_values, commit=False)
            db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    

    followed_posts = current_user.followed_posts()
    post_tags = {}
    post_votes = {}
    for post in followed_posts:
        post_tags[post.id] = post.get_tags()
        post_votes[post.id] = PostVote.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    
    # print(post_tags)
    page = request.args.get('page', 1, type=int)
    posts = followed_posts.paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    # print(posts.items)
    return render_template('index.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url,
                           all_tags=post_tags, tag_colors=group_colors, post_votes=post_votes,
                           prev_url=prev_url, office_extensions=app.config["OFFICE_EXTENSIONS"])


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None

    post_tags = {}
    post_votes = {}
    for post in Post.query.all():
        post_tags[post.id] = post.get_tags()
        post_votes[post.id] = PostVote.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    
    return render_template('index.html', title='Explore', posts=posts.items,
                            all_tags=post_tags, tag_colors=group_colors, post_votes=post_votes,
                            next_url=next_url, prev_url=prev_url, office_extensions=app.config["OFFICE_EXTENSIONS"])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form, office_extensions=app.config["OFFICE_EXTENSIONS"], vote=PostVote)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/post/<int:postid>', methods=['GET', 'POST'])
def get_post(postid):
    post = Post.query.get(postid)
    tags = post.get_tags_list()
    user_post_vote = PostVote.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    comment_form = AddCommentForm()
    if request.method == "POST" and comment_form.validate_on_submit(): # TODO: and is signed in 
        comment = Comment(body=comment_form.body.data, post_id=postid, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash("Your comment has been added to the post", "success")
    return render_template('post.html', post=post, form=comment_form, author=current_user, post_tags=tags, current_vote=user_post_vote)

@app.route('/database')
def database():
    return render_template(
        'database.html',
        title='Database',
        users=User.query.all(),
        # posts=Post.query.all(),
        course_groups=CourseGroup.query.all(),
        courses=Course.query.all(),
        units=Unit.query.all(),
        subunits=SubUnit.query.all(),
        subjects=Subject.query.all(),
        topics=Topic.query.all(),
        schools=School.query.all()
    )

@app.route('/_post_vote/<post_id>/<action_vote>', methods=['GET', 'POST'])
@login_required
def _post_vote(post_id, action_vote):
    post = Post.query.filter_by(id = post_id).first_or_404()
    vote = PostVote.query.filter_by(
        user_id = current_user.id,
        post_id = post_id).first()
    upvote = bool(int(action_vote))
    if vote is not None:
        # print("ALREADY VOTED")
        vote.upvote = upvote
        vote.timestamp = datetime.utcnow()
        db.session.commit()
        # return redirect(url_for('main._post', post_id = post.id))
    else:
        vote = PostVote(
            user_id=current_user.id,
            post_id=post_id,
            upvote=upvote
            )
        db.session.add(vote)
        db.session.commit()
        # flash('You already vote for this post')
        # return redirect(url_for('main._post', post_id = post.id))

    votes = post.votes_num()
    # print(f"#VOTED {votes}")
    return jsonify({'votes': votes})