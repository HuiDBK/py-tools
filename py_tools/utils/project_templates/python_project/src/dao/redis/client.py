from py_tools.connections.db.redis_client import BaseRedisManager


class RedisManager(BaseRedisManager):
    cache_key_prefix = ""
