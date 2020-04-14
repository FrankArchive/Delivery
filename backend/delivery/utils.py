import functools
import os

import requests
from flask import request, abort, session
from passlib.hash import bcrypt_sha256
from sqlalchemy.engine.url import make_url
from sqlalchemy_utils import create_database, database_exists

APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')


def get_user_openid(code):
    res = requests.get(
        'https://api.weixin.qq.com/sns/jscode2session',
        params={
            'appid': APP_ID,
            'secret': APP_SECRET,
            'js_code': code,
            'grant_type': 'authorization_code',
        }
    ).json()
    if 'errorcode' not in res.keys() or res['errorcode'] == 0:
        return res['openid']
    raise PermissionError('wx code error: ' + str(res['errmsg']))


def verify_keys(d: dict):
    def _verify_keys(func):
        @functools.wraps(func)
        def __verify_keys(*args, **kwargs):
            data = request.json
            if not data:
                abort(403)
            for k, t in d.items():
                if (k not in data.keys()) or (type(data[k]) != d[k]):
                    abort(
                        403,
                        'expected arguments: '+','.join(
                            [f'{i}: {j}' for i, j in d.items()]
                        )
                    )
            return func(*args, **kwargs)

        return __verify_keys

    return _verify_keys


def verify_captcha(func):
    @functools.wraps(func)
    def _verify_captcha(*args, **kwargs):
        req = request.json or request.form
        if 'captcha' not in session:
            abort(400, 'Captcha Session Invalid, start a session by calling /api/v1/captcha')
        if req['captcha'].lower() != session['captcha'].lower():
            session.pop('captcha')
            abort(400, 'Captcha Invalid')
        session.pop('captcha')
        return func(*args, **kwargs)

    return _verify_captcha


def authed(func):
    @functools.wraps(func)
    def _authed(*args, **kwargs):
        if 'user_id' not in session:
            abort(403)
        return func(*args, **kwargs)

    return _authed


def hash_password(plaintext):
    return bcrypt_sha256.hash(str(plaintext))


def verify_password(plaintext, ciphertext):
    return bcrypt_sha256.verify(plaintext, ciphertext)


def get_db():
    url = make_url(os.getenv('DB_URL') or 'sqlite:///test.db')
    if url.drivername.startswith('mysql'):
        url.query["charset"] = "utf8mb4"
    if not database_exists(url):
        if url.drivername.startswith("mysql"):
            create_database(url, encoding="utf8mb4")
        else:
            create_database(url)
    return url
