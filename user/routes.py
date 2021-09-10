from flask import Blueprint, jsonify, make_response, request
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

import models


user_blueprint = Blueprint('user_api_routes', __name__, url_prefix='/api/user')


@user_blueprint.route('/all', methods=['GET'])
def get_all_users():
    all_user = models.User.query.all()
    result = [user.serialize() for user in all_user]
    response = {
        'status': 'success',
        'message': 'return all users',
        'data': result
    }
    return jsonify(response)


@user_blueprint.route('/create', methods=['POST'])
def create_user():
    try:
        user = models.User()
        user.username = request.form['username']
        user.password = generate_password_hash(request.form['password'], method='sha256')
        user.is_admin = False
        models.db.session.add(user)
        models.db.session.commit()
        response = {'message': 'User Created', 'result': user.serialize()}
    except Exception as ex:
        response = {'message': 'User not Created', 'error': str(ex)}
    return jsonify(response)


@user_blueprint.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = models.User().query.filter_by(username=username).first()
    if not user:
        response = {'message': 'username or password doesnt match'}
        return make_response(jsonify(response), 401)
    if check_password_hash(user.password, password):
        user.generate_api_key()
        models.db.session.commit()
        login_user(user)
        response = {
            'message': 'user logged in',
            'api_key': user.api_key
        }
        return make_response(jsonify(response), 200)

    response = {'message': 'access denied'}
    return make_response(jsonify(response), 401)


@user_blueprint.route('/logout', methods=['POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({'message': 'user logged out'})
    return jsonify({'message': 'no user logged in'}), 401


@user_blueprint.route('/<username>/exists', methods=['GET'])
def user_exists(username):
    user = models.User.query.filter_by(username=username).first()
    if user:
        return jsonify({'result': True}), 200
    return jsonify({'result': False}), 404


@user_blueprint.route('/', methods=['GET'])
def get_current_user():
    if current_user.is_authenticated:
        return jsonify({'result': current_user.serialize()}), 200
    else:
        return jsonify({'result': 'user not logged in'}), 401
