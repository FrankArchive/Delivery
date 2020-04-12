import base64
import random

from captcha.image import ImageCaptcha
from flask import abort, request, session, current_app
from flask_restx import Namespace, Resource

from delivery.models import User, db
from delivery.utils import verify_keys, verify_password, verify_captcha, get_user_openid

users = Namespace("users")
generator = ImageCaptcha()


@users.route('captcha')
class Captcha(Resource):
    @staticmethod
    def get():
        captcha = ''.join(random.choices(
            '2345678abcdefhijkmnpqrstuvwxyzABCDEFGHJKLMNPRTUVXY', k=4
        ))
        img = generator.generate(captcha)
        session['captcha'] = captcha
        data = f'data:image/png;base64, {base64.b64encode(img.getvalue()).decode()}'
        if current_app.debug:
            return {'img': data, 'data': captcha}
        else:
            return {'img': data}


@users.route('login')
class Login(Resource):
    @verify_keys({
        'username': str, 'password': str,
        'captcha': str, 'code': str
        # 只有登陆的用户的open_id与当前微信号调用wx.login一致时才能登陆成功
    })
    @verify_captcha
    def post(self):
        req = request.json or {}
        user = User.query.filter_by(username=req['username']).first()
        if user is None:
            abort(403)
        if not verify_password(req['password'], user.password):
            abort(403, 'Wrong Password')
        code = request.json['code']
        open_id = get_user_openid(code)
        if user.open_id != open_id:
            abort(403, 'Wrong Wechat User')
        session['user_id'] = user.id
        return {}
        pass


@users.route('register')
class Register(Resource):
    @verify_keys({
        'username': str, 'password': str,
        'phone': str, 'captcha': str,
        'address': str,  # 用户的详细地址
        'code': str  # wx.login时返回的code
    })
    @verify_captcha
    def post(self):
        req = request.json
        if User.query.filter_by(username=req['username']).first():
            abort(403)
        db.session.add(User(**req))
        db.session.commit()
        return {}
