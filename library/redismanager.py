import redis
from configs.config import configs


class RedisManager:
    def __init__(self):
        redis_config = configs['redis']
        self.host = redis_config['host']
        self.port = redis_config['port']
        self.decode_responses = True

    def get_comm(self):
        pool = redis.ConnectionPool(host=self.host, port=self.port, decode_responses=True)
        conn = redis.Redis(connection_pool=pool)
        return conn


if __name__ == '__main__':
    conn = RedisManager().get_comm()
    ret = conn.set('test', 1)
    print(ret)
    print(conn.get('test'))
