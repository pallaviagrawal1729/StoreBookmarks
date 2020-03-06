from flask import render_template, flash, redirect, url_for,request
from bookmarkProject import app, db, login_manager
from flask_login import login_required, login_user, current_user, logout_user
from bookmarkProject.Form import BookmarkForm, LoginForm
from bookmarkProject.model import User, Bookmark


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", messages=Bookmark.new_bookmarks(5))


@app.route("/add", methods=['GET', 'POST'])
@login_required
def add():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        b = Bookmark(user=current_user, url=url, description=description)
        db.session.add(b)
        db.session.commit()
        # store_bookmark(url)
        flash("stored url: '{}' ".format(url))
        return redirect(url_for('index'))
    return render_template("add.html",form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('Logged in successfully as {}'.format(user.username))
            return redirect(request.args.get('next') or url_for('user', username=user.username))

        flash('Incorrect Username or password. Try again!')
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
