from core.hashing import Hasher


def test_hashing_and_verification():
    password = "mysecurepassword"

    hashed_password = Hasher.get_password_hash(password=password)
    assert Hasher.verify_password(
        plain_password=password,
        hashed_password=hashed_password) is True
    assert Hasher.verify_password(
        plain_password="wrongpassword",
        hashed_password=hashed_password) is False


def test_hash_salting():
    password = "samepassword"

    hash1 = Hasher.get_password_hash(password=password)
    hash2 = Hasher.get_password_hash(password=password)
    assert hash1 != hash2  # Different hashes due to salting
