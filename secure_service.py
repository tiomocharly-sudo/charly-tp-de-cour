#!/usr/bin/env python3
"""Version sécurisée du DocumentService - Exercice de durcissement"""

import Pyro5.api
import logging
import re
import time
from typing import Dict, List, Optional
from functools import wraps
from collections import defaultdict
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RateLimiter:
    """Rate limiter simple pour prévenir les attaques DoS"""
    
    def __init__(self, max_calls: int = 100, window_seconds: int = 60):
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self.calls: Dict[str, List[datetime]] = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> bool:
        now = datetime.now()
        # Nettoyer les anciennes entrées
        self.calls[client_id] = [
            t for t in self.calls[client_id]
            if now - t < timedelta(seconds=self.window_seconds)
        ]
        
        if len(self.calls[client_id]) >= self.max_calls:
            logger.warning(f"Rate limit exceeded for {client_id}")
            return False
        
        self.calls[client_id].append(now)
        return True


def validate_doc_id(func):
    """Décorateur de validation pour doc_id"""
    @wraps(func)
    def wrapper(self, doc_id, *args, **kwargs):
        if not isinstance(doc_id, str):
            raise ValueError("Identifiant invalide")
        if not (3 <= len(doc_id) <= 32):
            raise ValueError("Identifiant invalide")
        if not re.match(r'^[a-zA-Z0-9_]+$', doc_id):
            raise ValueError("Identifiant invalide")
        dangerous = ['..', '/', '\\', ';', '--', "'", '"']
        if any(d in doc_id for d in dangerous):
            raise ValueError("Identifiant invalide")
        return func(self, doc_id, *args, **kwargs)
    return wrapper


def log_call(func):
    """Décorateur de logging"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start = time.time()
        try:
            result = func(self, *args, **kwargs)
            elapsed = (time.time() - start) * 1000
            logger.info(f"{func.__name__}() - {elapsed:.2f}ms")
            return result
        except Exception as e:
            logger.error(f"{func.__name__}() - Erreur: {type(e).__name__}")
            raise
    return wrapper


@Pyro5.api.expose
class SecureDocumentService:
    """
    Version sécurisée du DocumentService avec:
    - Rate limiting
    - Validation stricte
    - Authentification
    - Logging détaillé
    - Messages d'erreur génériques
    """
    
    _VALID_TOKEN = "secure-tp10-2024-ensafes"
    
    def __init__(self):
        self._rate_limiter = RateLimiter(max_calls=50, window_seconds=60)
        self._access_count = 0
        self._error_count = 0
        
        # Base de données simulée
        self._documents = {
            "doc_001": {"content": "Rapport financier 2024", "confidential": True},
            "doc_002": {"content": "Guide utilisateur", "confidential": False},
            "doc_003": {"content": "Documentation API", "confidential": False},
        }
        logger.info("SecureDocumentService initialisé")
    
    def _check_auth(self, token: str) -> None:
        """Vérification d'authentification"""
        if not token or token != self._VALID_TOKEN:
            self._error_count += 1
            raise PermissionError("Accès non autorisé")
    
    def _check_rate_limit(self, client_info: str = "unknown") -> None:
        """Vérification rate limiting"""
        if not self._rate_limiter.is_allowed(client_info):
            self._error_count += 1
            raise RuntimeError("Trop de requêtes. Réessayez plus tard.")
    
    @log_call
    def list_documents(self, token: str = "") -> List[str]:
        """Liste les documents (version publique ou complète)"""
        self._access_count += 1
        self._check_rate_limit()
        
        if token and token == self._VALID_TOKEN:
            # Version authentifiée - tous les documents
            return list(self._documents.keys())
        else:
            # Version publique - uniquement non confidentiels
            return [doc_id for doc_id, data in self._documents.items()
                   if not data.get("confidential", False)]
    
    @log_call
    @validate_doc_id
    def get_document_content(self, doc_id: str, token: str = "") -> str:
        """Récupère le contenu d'un document"""
        self._access_count += 1
        self._check_rate_limit()
        
        # Vérifier existence
        if doc_id not in self._documents:
            self._error_count += 1
            raise KeyError("Document introuvable")  # Message générique
        
        doc = self._documents[doc_id]
        
        # Vérifier confidentialité
        if doc.get("confidential", False):
            self._check_auth(token)
        
        logger.info(f"Document servi: {doc_id}")
        return doc["content"]
    
    @log_call
    def get_stats(self, token: str) -> Dict:
        """Statistiques du service (nécessite authentification)"""
        self._check_auth(token)
        self._check_rate_limit()
        
        return {
            "access_count": self._access_count,
            "error_count": self._error_count,
            "documents_available": len(self._documents),
            "status": "operational"
        }
    
    def _reload_index(self):
        """Méthode interne - NON exposée"""
        logger.warning("Tentative d'accès à _reload_index")
        pass
    
    def _get_db_connection(self):
        """Méthode interne - NON exposée"""
        logger.warning("Tentative d'accès à _get_db_connection")
        pass


def main():
    """Démarre le service sécurisé"""
    with Pyro5.api.Daemon() as daemon:
        try:
            ns = Pyro5.api.locate_ns()
            uri = daemon.register(SecureDocumentService)
            ns.register("bank.documents.secure", uri)
            
            logger.info("="*60)
            logger.info("SECURE DOCUMENT SERVICE DÉMARRÉ")
            logger.info(f"URI: {uri}")
            logger.info("="*60)
            
            daemon.requestLoop()
        except Exception as e:
            logger.error(f"Erreur: {e}")


if __name__ == "__main__":
    main()