import Pyro5.api

AUTH_TOKEN = "secure-tp10-2024"

def main():
    try:
        ns = Pyro5.api.locate_ns()
        uri = ns.lookup("bank.documents.service")
        
        with Pyro5.api.Proxy(uri) as service:
            print("\n=== TEST DOCUMENT SERVICE ===\n")
            
            print("1. Documents publics:")
            docs = service.list_documents()
            for d in docs:
                print(f"   - {d}")
            
            print("\n2. Lecture doc_002:")
            print(f"   {service.get_document_content('doc_002')}")
            
            print("\n3. Lecture doc_001 (sans auth):")
            try:
                print(f"   {service.get_document_content('doc_001')}")
            except Exception as e:
                print(f"   ❌ {e}")
            
            print("\n4. Lecture doc_001 (avec auth):")
            print(f"   ✅ {service.get_document_content('doc_001', AUTH_TOKEN)}")
            
            print("\n=== TEST RÉUSSI ===\n")
            
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    main()