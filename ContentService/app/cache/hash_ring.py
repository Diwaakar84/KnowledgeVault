import hashlib
import bisect

# Consistent hashing implementation
class ConsistentHashRing:
    def __init__(self, nodes=None, replicas=100):
        self.replicas = replicas
        self.ring = dict()
        self.sorted_keys = []

        if nodes:
            for node in nodes:
                self.add_node(node)

    # Hash funtion for the hash ring used to locate a data
    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16)

    # Insert a node into the hash ring
    def add_node(self, node: str):
        for i in range(self.replicas):
            virtual_node = f"{node}#{i}"
            h = self._hash(virtual_node)
            self.ring[h] = node
            bisect.insort(self.sorted_keys, h)

    # Remove a node from the hash ring
    def remove_node(self, node: str):
        for i in range(self.replicas):
            virtual_node = f"{node}#{i}"
            h = self._hash(virtual_node)
            if h in self.ring:
                del self.ring[h]
                self.sorted_keys.remove(h)

    # Fetch a node present in the hash ring
    def get_node(self, key: str) -> str:
        if not self.ring:
            return None

        h = self._hash(key)
        idx = bisect.bisect(self.sorted_keys, h)

        if idx == len(self.sorted_keys):
            idx = 0

        return self.ring[self.sorted_keys[idx]]
