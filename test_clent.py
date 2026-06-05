#!/usr/bin/env python3
"""Script de test complet pour DocumentService"""

import Pyro5.api
import sys
import time

AUTH_TOKEN = "secure-tp10-2024-ensafes"


def test_public_access():
    """Test accès public"""
    print("\n" + "="*60)
    print("TEST 1: ACCÈS PUBLIC")
    print("="*60)
    
    ns = Pyro5.api.locate_ns()
    uri = ns.lookup("bank.documents.service")
    
    with Pyro5.api.Proxy(uri) as proxy:
        # Liste publique
        docs = proxy.list_documents()
        print(f"Documents publics: {docs}")
        
        # Accès document public
        content = proxy.get_document_content("doc_002")
        print(f"doc_002: {content[:50]}...")


def test_authenticated_access():
    """Test accès authentifié"""
    print("\n" + "="*60)
    print("TEST 2: ACCÈS AUTHENTIFIÉ")
    print("="*60)
    
    ns = Pyro5.api.locate_ns()
    uri = ns.lookup("bank.documents.service")
    
    with Pyro5.api.Proxy(uri) as proxy:
        # Liste complète
        docs = proxy.list_documents(AUTH_TOKEN)
        print(f"Tous les documents: {docs}")
        
        # Accès document confidentiel
        content = proxy.get_document_content("doc_001", AUTH_TOKEN)
        print(f"doc_001 (confidentiel): {content[:50]}...")


def test_validation():
    """Test validation des entrées"""
    print("\n" + "="*60)
    print("TEST 3: VALIDATION DES ENTRÉES")
    print("="*60)
    
    ns = Pyro5.api.locate_ns()
    uri = ns.lookup("bank.documents.service")
    
    test_cases = [
        ("../../etc/passwd", "Path traversal"),
        ("doc;DROP", "Injection SQL"),
        ("a"*100, "Trop long"),
        ("", "Vide"),
        ("doc_id", "Valide"),
        ("12345", "Numérique seul"),
        ("doc@#$", "Caractères spéciaux"),
    ]
    
    with Pyro5.api.Proxy(uri) as proxy:
        for doc_id, description in test_cases:
            try:
                result = proxy.get_document_content(doc_id)
                print(f"  {description:20} '{doc_id[:20]}' → {result[:40]}")
            except Exception as e:
                print(f"  {description:20} '{doc_id[:20]}' → REJETÉ: {e}")


def test_error_handling():
    """Test gestion des erreurs"""
    print("\n" + "="*60)
    print("TEST 4: GESTION DES ERREURS")
    print("="*60)
    
    ns = Pyro5.api.locate_ns()
    uri = ns.lookup("bank.documents.service")
    
    with Pyro5.api.Proxy(uri) as proxy:
        # Document inexistant
        try:
            proxy.get_document_content("doc_999")
        except Exception as e:
            print(f"Document inexistant: {type(e).__name__} - {e}")
        
        # Type invalide
        try:
            proxy.get_document_content(12345)
        except Exception as e:
            print(f"Type invalide: {type(e).__name__} - {e}")
        
        # Token invalide pour doc confidentiel
        try:
            proxy.get_document_content("doc_001", "wrong_token")
        except Exception as e:
            print(f"Token invalide: {type(e).__name__} - {e}")


def test_internal_methods():
    """Test que les méthodes internes ne sont PAS exposées"""
    print("\n" + "="*60)
    print("TEST 5: MÉTHODES INTERNES NON EXPOSÉES")
    print("="*60)
    
    ns = Pyro5.api.locate_ns()
    uri = ns.lookup("bank.documents.service")
    
    with Pyro5.api.Proxy(uri) as proxy:
        internal_methods = ["_reload_index", "_get_db_connection", "_check_token"]
        
        for method in internal_methods:
            try:
                # Tenter d'appeler la méthode interne
                getattr(proxy, method)()
                print(f"  ⚠️ {method} est accessible!")
            except AttributeError:
                print(f"  ✅ {method} n'est PAS accessible")
            except Exception as e:
                print(f"  ℹ️ {method}: {type(e).__name__}")


def performance_test():
    """Test de performance simple"""
    print("\n" + "="*60)
    print("TEST 6: PERFORMANCE")
    print("="*60)
    
    ns = Pyro5.api.locate_ns()
    uri = ns.lookup("bank.documents.service")
    
    n_calls = 20
    start = time.time()
    
    with Pyro5.api.Proxy(uri) as proxy:
        for i in range(n_calls):
            proxy.list_documents()
    
    elapsed = time.time() - start
    print(f"{n_calls} appels en {elapsed:.2f}s")
    print(f"Moyenne: {elapsed/n_calls*1000:.1f}ms/appel")


def main():
    """Exécute tous les tests"""
    print("\n" + "="*60)
    print("DOCUMENT SERVICE - SUITE DE TESTS")
    print("="*60)
    
    tests = [
        ("Accès public", test_public_access),
        ("Accès authentifié", test_authenticated_access),
        ("Validation entrées", test_validation),
        ("Gestion erreurs", test_error_handling),
        ("Méthodes internes", test_internal_methods),
        ("Performance", performance_test),
    ]
    
    for name, test_func in tests:
        try:
            test_func()
        except Exception as e:
            print(f"\n❌ Test '{name}' échoué: {e}")
    
    print("\n" + "="*60)
    print("TESTS TERMINÉS")
    print("="*60)


if __name__ == "__main__":
    main()