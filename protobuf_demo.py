import json

print("\n" + "="*50)
print("TP7.3 - PROTOCOL BUFFERS")
print("="*50)

print("""
Concept de Protobuf:
- Un fichier .proto définit le schéma
- protoc génère du code Python
- SerializeToString() -> bytes
- ParseFromString() -> objet

Exemple de schéma document.proto:
    syntax = "proto3";
    message Document {
        int32 id = 1;
        string title = 2;
        string author = 3;
        repeated string tags = 4;
        string classification = 5;
    }

Avantages:
- Encodage binaire compact
- Validation de types intégrée
- Versioning natif (champs numérotés)
""")

data = {"id": 42, "title": "Rapport", "author": "Alice", "tags": ["finance"]}
json_bytes = json.dumps(data).encode('utf-8')
print(f"\n📊 Comparaison: JSON = {len(json_bytes)} octets")
print("   Protobuf = environ 50-60 octets (2-3x plus compact)")