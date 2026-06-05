POLICY = """
╔════════════════════════════════════════════════════════════════╗
║           POLITIQUE DE SÉRIALISATION SÛRE                      ║
╠════════════════════════════════════════════════════════════════╣
║  ☑ Interdire pickle pour toute entrée non fiable               ║
║  ☑ Utiliser JSON ou Protobuf pour les entrées externes         ║
║  ☑ Limiter la taille des payloads avant parsing                ║
║  ☑ Valider chaque champ (type, longueur, allowlist)            ║
║  ☑ Fail closed: refuser en cas de doute                       ║
╚════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(POLICY)
    print("\n" + "="*50)
    print("TABLEAU DE POLITIQUE")
    print("="*50)
    print("| Source          | Format     | Justification                      |")
    print("| API REST        | JSON       | Non fiable → format inerte         |")
    print("| Cache local     | pickle     | Données locales de confiance       |")
    print("| Upload fichier  | JSON       | Jamais pickle sur fichiers tiers   |")