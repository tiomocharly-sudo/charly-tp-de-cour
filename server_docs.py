import Pyro5.api
import re

_DOCUMENTS = {
    "doc_001": "Document CONFIDENTIEL - Rapport financier 2024",
    "doc_002": "Document PUBLIC - Guide utilisateur",
    "doc_003": "Document PUBLIC - Documentation API",
}

@Pyro5.api.expose
class DocumentService:
    _TOKEN = "secret123"
    
    def list_documents(self, token=""):
        if token == self._TOKEN:
            return list(_DOCUMENTS.keys())
        return ["doc_002", "doc_003"]
    
    def get_document_content(self, doc_id, token=""):
        if doc_id not in _DOCUMENTS:
            raise KeyError("Document introuvable")
        if doc_id == "doc_001" and token != self._TOKEN:
            raise PermissionError("Accès refusé - document confidentiel")
        return _DOCUMENTS[doc_id]

with Pyro5.api.Daemon() as daemon:
    ns = Pyro5.api.locate_ns()
    uri = daemon.register(DocumentService())
    ns.register("doc.service", uri)
    print(f"Serveur OK: {uri}")
    daemon.requestLoop()