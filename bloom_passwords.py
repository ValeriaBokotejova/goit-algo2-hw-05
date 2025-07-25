"""
Task 1: Password uniqueness check using Bloom Filter.

Provides:
- class BloomFilter(size: int, num_hashes: int)
- function check_password_uniqueness(bloom: BloomFilter, passwords: list[str]) -> dict[str, str]
"""

import hashlib
from typing import List, Dict

class BloomFilter:
    def __init__(self, size: int, num_hashes: int):
        if not isinstance(size, int) or size <= 0:
            raise ValueError("size must be a positive integer")
        if not isinstance(num_hashes, int) or num_hashes <= 0:
            raise ValueError("num_hashes must be a positive integer")
        self.size = size
        self.num_hashes = num_hashes
        self.bits = [False] * size

    def _hashes(self, item: str):
        for i in range(self.num_hashes):
            data = f"{item}:{i}".encode("utf-8")
            digest = hashlib.sha256(data).hexdigest()
            yield int(digest, 16) % self.size

    def add(self, item: str) -> None:
        if not isinstance(item, str):
            raise TypeError("BloomFilter.add: item must be a string")
        for idx in self._hashes(item):
            self.bits[idx] = True

    def __contains__(self, item: str) -> bool:
        if not isinstance(item, str):
            raise TypeError("BloomFilter.__contains__: item must be a string")
        return all(self.bits[idx] for idx in self._hashes(item))


def check_password_uniqueness(bloom: BloomFilter, passwords: List[str]) -> Dict[str, str]:
    if not isinstance(passwords, list):
        raise TypeError("passwords must be a list of strings")

    result = {}
    for pw in passwords:
        if not isinstance(pw, str):
            status = "invalid input"
        elif pw in bloom:
            status = "already used"
        else:
            status = "unique"
            bloom.add(pw)
        result[pw] = status

    return result


if __name__ == "__main__":
    # Example usage
    bloom = BloomFilter(size=1000, num_hashes=3)
    existing = ["password123", "admin123", "qwerty123"]
    for pw in existing:
        bloom.add(pw)

    new_list = ["password123", "newpassword", "admin123", "guest"]
    res = check_password_uniqueness(bloom, new_list)
    for pw, status in res.items():
        print(f"Password '{pw}' - {status}.")
