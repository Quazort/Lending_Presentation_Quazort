from collections import defaultdict
import time


class RateLimitRepository:
    def __init__(self):
        self._storage = defaultdict(list)

    def is_rate_limited(self, ip: str, limit: int, window: int) -> bool:
        now = time.time()

        self._storage[ip] = [t for t in self._storage[ip] if now - t < window]

        if len(self._storage[ip]) >= limit:
            return True

        self._storage[ip].append(now)
        return False


rate_limit_repo = RateLimitRepository()
