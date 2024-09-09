from hashlib import sha256

class Hasher:
    @staticmethod
    def verify_hash(plain: str, hashed: str) -> bool:
        return Hasher.get_hash(plain) == hashed

    @staticmethod
    def get_hash(source: str) -> str:
        return sha256(source.encode()).hexdigest()