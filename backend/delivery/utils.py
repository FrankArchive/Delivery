import functools

from flask import request, abort
from passlib.hash import bcrypt_sha256


def verify_keys(d: dict):
    def _verify_keys(func):
        @functools.wraps(func)
        def __verify_keys(*args, **kwargs):
            data = request.json
            if not data:
                abort(403)
            for k, t in d.items():
                if (k not in data.keys()) or (type(data[k]) != d[k]):
                    abort(403)
            return func(*args, **kwargs)

        return __verify_keys

    return _verify_keys


def hash_password(plaintext):
    return bcrypt_sha256.hash(str(plaintext))


def verify_password(plaintext, ciphertext):
    return bcrypt_sha256.verify(plaintext, ciphertext)
