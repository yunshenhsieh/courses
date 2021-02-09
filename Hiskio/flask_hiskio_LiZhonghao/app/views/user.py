from flask import render_template, request
from app.models.user import User, _create, _update, _destroy
class views:
    def index():
        return render_template('users/index.html')

    def new():
        user = User()
        return render_template('users/new.html', user=user)

    def create():
        username = request.form['username']
        email = request.form['email']
        # call models
        _create(username, email)
        return "User creation successful"

    def show(id):
        user = User.query.filter_by(id=id).first()
        return render_template('users/show.html', user=user)

    def edit(id, url_delete):
        user = User.query.filter_by(id=id).first()
        return render_template('users/edit.html', user=user, url_delete=url_delete)

    def update(id):
        email = request.form['email']
        _update(id,email)
        return

    def destroy(id):
        _destroy(id)
        return