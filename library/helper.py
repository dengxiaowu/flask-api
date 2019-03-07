from controllers.base import Base
# from library.crypthelper import Crypter
from cryptography.fernet import Fernet


def debug(data):
    return Base().ret_json(1, 'ok', data)


def varify_password(password, jiami_password):
    f = Fernet(__get_password_key())
    if type(b'') != type(jiami_password):
        jiami_password = jiami_password.encode()
    jiemi_pass = f.decrypt(jiami_password)
    if jiemi_pass == password.encode():
        return True
    else:
        return False


def get_password(password):
    f = Fernet(__get_password_key())
    if type(b'') != type(password):
        password = password.encode()
    jiami_pass = f.encrypt(password)
    if jiami_pass:
        return jiami_pass.decode('utf-8')
    else:
        return False


def __get_password_key():
    return b'9rVqEgVoVyAj7ioAmZaaj5Bg3DniWZjxghlWTEOXCzM='


if __name__ == '__main__':
    jiami = get_password(b'12345')
    print(jiami)
    jiami3 = get_password(b'12345')
    print(jiami3)
    jiami2 = get_password(b'877hjdxujukah1')
    print(jiami2)
    print(len(jiami2) == len(jiami))
    print(len(jiami2))
    print(varify_password(b'12345', jiami))
