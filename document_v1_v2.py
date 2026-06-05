import json

class DocumentDeserializerV2:
    @classmethod
    def deserialize(cls, raw: str) -> dict:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            raise ValueError("Payload invalide")
        
        errors = []
        
        for field in ["id", "title", "author"]:
            if field not in data:
                errors.append(f"Champ manquant: {field}")
        
        if "id" in data and (not isinstance(data["id"], int) or data["id"] <= 0):
            errors.append("'id' invalide")
        
        tags = data.get("tags", [])
        if not isinstance(tags, list):
            errors.append("'tags' doit être une liste")
        
        classification = data.get("classification", "internal")
        if classification not in {"public", "internal", "confidential", "secret"}:
            errors.append(f"classification non autorisée: {classification}")
        
        if errors:
            raise ValueError("Payload invalide")
        
        return {
            "id": data["id"],
            "title": data["title"],
            "author": data["author"],
            "tags": tags,
            "classification": classification,
        }

if __name__ == "__main__":
    print("\n" + "="*50)
    print("TP7.2 - VERSIONING JSON")
    print("="*50)
    
    v1 = '{"id": 1, "title": "Rapport", "author": "Alice"}'
    print(f"\n Payload v1: {v1}")
    result = DocumentDeserializerV2.deserialize(v1)
    print(f"   -> Résultat: {result}")
    
    v2 = '{"id": 2, "title": "Note", "author": "Bob", "tags": ["urgent"], "classification": "confidential"}'
    print(f"\n Payload v2: {v2}")
    result = DocumentDeserializerV2.deserialize(v2)
    print(f"   -> Résultat: {result}")