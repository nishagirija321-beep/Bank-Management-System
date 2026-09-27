import hashlib

def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

def verify_pin(pin,hashed_pin):
    return hash_pin(pin) == hashed_pin