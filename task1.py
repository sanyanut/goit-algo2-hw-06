import mmh3


class BloomFilter:
    def __init__(self, size=1000, num_hashes=3):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def _get_hash_indices(self, item: str) -> list:
        indices = []
        for i in range(self.num_hashes):
            hash_value = mmh3.hash(item, i, signed=False)
            indices.append(hash_value % self.size)
        return indices

    def add(self, item: str):
        if not item or not isinstance(item, str):
            return

        for idx in self._get_hash_indices(item):
            self.bit_array[idx] = True

    def contains(self, item: str) -> bool:
        if not item or not isinstance(item, str):
            return False

        for idx in self._get_hash_indices(item):
            if not self.bit_array[idx]:
                return False
        return True


def check_password_uniqueness(bloom_filter: BloomFilter, passwords: list) -> dict:
    results = {}
    for pwd in passwords:
        if not isinstance(pwd, str) or not pwd.strip():
            results[pwd] = "invalid value"
            continue

        if bloom_filter.contains(pwd):
            results[pwd] = "already used"
        else:
            results[pwd] = "unique"

    return results


if __name__ == "__main__":
    bloom = BloomFilter(size=1000, num_hashes=3)

    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    check_results = check_password_uniqueness(bloom, new_passwords_to_check)

    for password, status in check_results.items():
        print(f"Password '{password}' - {status}")