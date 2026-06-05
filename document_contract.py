import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any

ALLOWED_CLASSIFICATIONS = {"public", "internal", "confidential", "secret"}

@dataclass
class Document:
    id: int
    title: str
    author: str
    tags: List[str] = field(default_factory=list)
    classification: str = "internal"

def validate_document(data: Dict[str, Any]) -> Dict[str, Any]:
    errors = []
    
    if not isinstance(data, dict):
        raise ValueError("Payload invalide")
    
    for field in ["id", "title", "author"]:
        if field not in data:
            errors.append(f"Champ manquant: {field}")
    
    if "id" in data and (not isinstance(data["id"], int) or data["id"] <= 0):
        errors.append("'id' doit être un entier positif")
    
    if "title" in data:
        if not isinstance(data["title"], str) or len(data["title"].strip()) == 0:
            errors.append("'title' invalide")
    
    if "classification" in data and data["classification"] not in ALLOWED_CLASSIFICATIONS:
        errors.append(f"classification non autorisée: {data['classification']}")
    
    if errors:
        raise ValueError("Payload invalide")
    
    return data

def deserialize_document(raw: str) -> Document:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError("Payload invalide")
    
    validated = validate_document(data)
    
    return Document(
        id=validated["id"],
        title=validated["title"].strip(),
        author=validated["author"].strip(),
        tags=validated.get("tags", []),
        classification=validated.get("classification", "internal"),
    )

def serialize_document(doc: Document) -> str:
    return json.dumps(asdict(doc), ensure_ascii=False, indent=2)

if __name__ == "__main__":
    print("\n" + "="*50)
    print("TP7.1 - CONTRAT JSON")
    print("="*50)
    
    doc = Document(id=42, title="Rapport Q1", author="Alice", tags=["finance"])
    json_str = serialize_document(doc)
    print(f"\n✅ Document sérialisé:\n{json_str}")
    
    doc2 = deserialize_document(json_str)
    print(f"✅ Désérialisé: {doc2}")
    
    print("\n❌ Test payload invalide:")
    try:
        deserialize_document('{"id": "abc", "title": 123}')
    except ValueError as e:
        print(f"   Rejeté: {e}")