import pytest
from scripts.cortex.indexer import compute_hash

def test_compute_hash_deterministic():
    """Test that the same input always produces the same hash."""
    content = "hello world"
    hash1 = compute_hash(content)
    hash2 = compute_hash(content)
    assert hash1 == hash2

def test_compute_hash_different_inputs():
    """Test that different inputs produce different hashes."""
    hash1 = compute_hash("input A")
    hash2 = compute_hash("input B")
    assert hash1 != hash2

def test_compute_hash_length():
    """Test that the hash produces a 32-character string (digest_size=16 * 2 hex chars)."""
    content = "test content"
    hash_val = compute_hash(content)
    assert len(hash_val) == 32

def test_compute_hash_non_ascii():
    """Test that non-ASCII characters are handled correctly."""
    content = "한글 테스트 🚀"
    hash_val = compute_hash(content)
    assert len(hash_val) == 32
    # Ensure it's deterministic even with non-ASCII
    assert hash_val == compute_hash(content)

def test_compute_hash_empty_string():
    """Test that an empty string can be hashed."""
    hash_val = compute_hash("")
    assert len(hash_val) == 32

def test_compute_hash_known_value():
    """Test against a known expected hash computation method."""
    import hashlib
    content = "known test string"
    # The current implementation uses blake2b with digest_size=16
    expected = hashlib.blake2b(content.encode("utf-8"), digest_size=16).hexdigest()
    assert compute_hash(content) == expected
