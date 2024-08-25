import bcrypt

import bcrypt

def hash_password(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed


def check_password(hashed, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

