from flask import Blueprint, request
import utils
import hashlib

credentials = Blueprint('credentials', __name__)

@credentials.route('/login')
def login():
    username = request.form.get('username') or request.args.get('username')
    password = request.form.get('password') or request.args.get('password')
    if not username or not password:
        return utils.error_page(['insufficient parameters', 'username', 'password'])
    username = username.replace('"', '')
    password = hashlib.md5(
        password.encode()
    ).hexdigest()

    cursor = utils.db_execute(f'select password,roal from user where username="{username}"')
    result = cursor.fetchone()
    if result == None:
        return utils.error_page(['no such user'])
    if password != result[0]:
        return utils.error_page(['wrong password'])
    return result[1]

@credentials.route('/register')
def register():
    username = request.form.get('username').replace('"', '')
    password = request.form.get('password').encode()
    
    if len(password) < '6':
        return utils.error_page(['password too short'])

    password = hashlib.md5(
        password
    ).hexdigest()
    utils.db_execute(f'insert into user (username, password) values ("{username}", "{password}")')
    return 'ok'