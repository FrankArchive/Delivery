import base64
import random

from captcha.image import ImageCaptcha
from flask import abort, request, session
from flask_restplus import Namespace, Resource

from delivery.models import User, db
from delivery.utils import verify_keys, verify_password, hash_password

users = Namespace("users")
generator = ImageCaptcha()


@users.route('captcha')
class Captcha(Resource):
    @staticmethod
    def get():
        captcha = ''.join(random.choices(
            '2345678abcdefhijkmnpqrstuvwxyzABCDEFGHJKLMNPQRTUVWXY', k=4
        ))
        img = generator.generate(captcha)
        session['captcha'] = captcha
        data = f'data:image/png;base64, {base64.b64encode(img.getvalue()).decode()}'
        return {'img': data, 'data': captcha}


@users.route('login')
class Login(Resource):
    @verify_keys({
        'username': str, 'password': str,
        'captcha': str,
    })
    def post(self):
        req = request.json
        if 'captcha' not in session or req['captcha'] != session['captcha']:
            abort(400)
        session.pop('captcha')
        user = User.query.filter_by(username=req['username']).first()
        if user is None:
            abort(403)
        if not verify_password(req['password'], user.password):
            abort(403)
        session['user_id'] = user.id
        return {}


@users.route('register')
class Register(Resource):
    @verify_keys({
        'username': str, 'password': str,
        'phone': str, 'captcha': str
    })
    def post(self):
        req = request.json
        if 'captcha' not in session or req['captcha'] != session['captcha']:
            abort(400)
        session.pop('captcha')
        if User.query.filter_by(username=req['username']).first():
            abort(403)
        db.session.add(User(**req))
        db.session.commit()
        return {}
