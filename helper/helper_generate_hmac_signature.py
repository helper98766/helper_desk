def generate_hmac_signature(algorithm: str, stringToSign: str, secrert_key: str) -> str:
    hmac = hmac.new(secrert_key.encode(), stringToSign.encode(), hashlib.new(algorithm))
    signature = hmac.hexdigest()
    return signature