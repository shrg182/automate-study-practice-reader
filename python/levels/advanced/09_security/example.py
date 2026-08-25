import hmac
from hashlib import sha256

def sign(message, secret): return hmac.new(secret, message, sha256).hexdigest()
if __name__ == "__main__": print(sign(b"reader-export", b"demo-only-secret"))
