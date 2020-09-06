from flask import Blueprint, render_template, request, jsonify, send_from_directory, current_app
from models.admin.admin import Admin
from models.user.user import User
from models.user.decorators import requires_login
from models.admin.decorators import role_required
import os

admin = Blueprint('admin', __name__)


@admin.before_request
@requires_login
@role_required('admin')
def before_request():
    """ Protect all of the admin endpoints. """
    pass


@admin.route('/', methods=['GET', 'POST'])
def admin_dashboard():
    return render_template("admin.html")


@admin.route('/users/list/',  defaults={'query': None})
@admin.route('/users/list/<query>')
def get_users(query):

    if query:
        users_list = Admin.get_users(query=query)
    else:
        users_list = Admin.get_users(query=None)

    data = []
    if users_list:
        for user in users_list:
            data.append(user)

    return jsonify(data), 200


@admin.route('/users/delete/', methods=['POST'])
def delete_users():
    data = request.get_json(force=True)
    response = {'status': 'Unable to make changes.'}
    if len(data['data']) > 0:
        if Admin.delete_user(list_of_users=data['data']):
            response = {'status': 'success'}

    return jsonify(response), 200


@admin.route('/users/update/', methods=['POST'])
def update_users():
    data = request.get_json()
    print(data)
    user = User.find_by_id(_id=data['_id'])
    user.name = data['name']
    user.email = data['email']
    user.company = data['company']
    user.role = data['role']
    user.image = data['image']
    user.update_user()

    response = {'status': True}

    return jsonify(response), 200


@admin.route('users/export/', defaults={'query': None})
@admin.route('users/export/<query>')
def export_user(query):
    file_name = Admin.export_user(query=query)
    directory = os.path.join(current_app.config['EXPORT_PATH'])
    print(directory)
    try:
        return send_from_directory(directory=directory, filename=file_name, as_attachment=True)
    except Exception as e:
        return str(e)


