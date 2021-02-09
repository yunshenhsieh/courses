from app import app
from app.views.user import views
from flask import url_for

@app.route('/', methods=['GET'])
def index():
    return views.index()

@app.route('/new', methods=['GET'])
def new():
    return views.new()

@app.route('/create', methods=['POST'])
def create():
    return views.create()

@app.route('/<int:id>', methods=['GET'])
def show(id):
    return views.show(id)

@app.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    url_delete = url_for("destroy", id=id)
    return views.edit(id, url_delete = url_delete)

@app.route('/<int:id>', methods=['POST'])
def update(id):
    views.update(id)
    return "User update successful"

@app.route('/<int:id>/delete', methods=['POST'])
def destroy(id):
    views.destroy(id)
    return "User deleted!"

if __name__ == '__main__':
    app.run(debug=True)