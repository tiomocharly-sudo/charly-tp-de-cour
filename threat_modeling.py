import hmac
import hashlib
import json
import time

THREATS = [
    ("Tampering", "Altération du payload", "HMAC/TLS", "CRITIQUE"),
    ("Injection", "Ajout de champs malveillants", "Allowlist", "ÉLEVÉE"),
    ("Replay", "Rejeu d'un payload capturé", "Timestamp", "MOYENNE"),
    ("Pickle RCE", "Exécution code via pickle", "Interdire pickle", "CRITIQUE"),
]

class SecureSerializer:
    def __init__(self, secret: bytes):
        self.secret = secret
    
    def serialize(self, data: dict) -> tuple:
        data["_ts"] = int(time.time())
        payload = json.dumps(data, sort_keys=True)
        sig = hmac.new(self.secret, payload.encode(), hashlib.sha256).hexdigest()
        return payload, sig
    
    def deserialize(self, payload: str, sig: str, max_age: int = 60) -> dict:
        expected = hmac.new(self.secret, payload.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, sig):
            raise ValueError("Signature invalide")
        data = json.loads(payload)
        if time.time() - data["_ts"] > max_age:
            raise ValueError("Timestamp expiré")
        return data

if __name__ == "__main__":
    print("\n" + "="*50)
    print("LAB SÉCURITÉ - THREAT MODELING")
    print("="*50)
    
    print("\n🔴 MATRICE DES MENACES")
    for t in THREATS:
        print(f"   [{t[3]}] {t[0]}: {t[1]} → {t[2]}")
    
    print("\n🔐 DÉMONSTRATION HMAC + TIMESTAMP")
    serializer = SecureSerializer(b"secret_key")
    data = {"user": "alice", "action": "read"}
    payload, sig = serializer.serialize(data)
    print(f"   Payload: {payload}")
    print(f"   Signature: {sig[:32]}...")
    
    decoded = serializer.deserialize(payload, sig)
    print(f"   ✅ Vérifié: {decoded}")