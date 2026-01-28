import redis
from app.cache.hash_ring import ConsistentHashRing

REDIS_NODES = [
    "redis://localhost:6379/0",
    "redis://localhost:6379/1",
    "redis://localhost:6379/2",
]

class ShardedRedis:
    # Router for the hash ring
    # Finds which redis ring owns the requested data and returns it
    def __init__(self, nodes):
        self.ring = ConsistentHashRing(nodes)
        self.clients = {
            node: redis.Redis.from_url(node, decode_responses=True)
            for node in nodes
        }

    def _get_client(self, key: str):
        node = self.ring.get_node(key)
        return self.clients[node]

    def get(self, key: str):
        client = self._get_client(key)
        return client.get(key)

    def setex(self, key: str, ttl: int, value: str):
        client = self._get_client(key)
        return client.setex(key, ttl, value)

    def delete(self, key: str):
        client = self._get_client(key)
        return client.delete(key)
