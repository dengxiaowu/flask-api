import time

import jwt

from library.logmanager import AppLog


# from library.redismanager import RedisManager


class TokenManager:

    def __init__(self):
        self.secret = 'secret'
        self.payload = {
            "iat": int(time.time()),
            "exp": int(time.time()) + 7 * 86400
        }

    # self.redis_conn = RedisManager().get_comm()

    # 获取token
    def get_token(self, user_id, username):

        self.payload["user_id"] = user_id
        self.payload["username"] = username

        token = jwt.encode(self.payload, self.secret, algorithm='HS256').decode('utf-8')
        if token:
            # 保存redis
            # self.redis_conn.set(token, 1)
            return token
        else:
            return ''

    # 验证token
    def verify_token(self, token):
        try:

            self.payload = jwt.decode(token, self.secret, algorithm='HS256')
            if self.payload:
                exp_time = self.payload["exp"]
                now_time = time.time()
                if exp_time < now_time:
                    return False
                else:
                    return self.payload
            else:
                return False
        except Exception as e:
            AppLog('test').error(e)
            return False

    # 刷新登录token
    def fresh_token(self, token):

        result = self.verify_token(token)
        if result:
            # 删除
            # self.redis_conn.delete(token)
            user_id = result["user_id"]
            username = result["username"]

            new_token = self.get_token(user_id, username)
            # self.redis_conn.set(new_token, 1)
            if new_token:
                return new_token
            else:
                return False
        else:
            return False

    # 删除token
    def del_token(self, token):
        return  # self.redis_conn.delete(token)


if __name__ == '__main__':
    token_handle = TokenManager()
    token1 = token_handle.get_token(123, 'xiaowu')
    print(token1)
    ret = token_handle.verify_token(token1)
    print(ret)
