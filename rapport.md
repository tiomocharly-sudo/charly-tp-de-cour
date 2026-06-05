# TP7 - Sérialisation et Marshalling en Python

## Introduction

Ce rapport présente l'implémentation des concepts de sérialisation et marshalling.

## Partie 1 - Contrat JSON

### Résultats des tests

| Test | Résultat |
|------|----------|
| Document valide complet | ✅ Accepté |
| Document valide minimal | ✅ Accepté |
| ID manquant | ❌ Rejeté |
| ID négatif | ❌ Rejeté |
| ID string | ❌ Rejeté |
| Champ inconnu | ❌ Rejeté |

## Partie 2 - Versioning JSON

Stratégie: ajout de champs optionnels uniquement, valeurs par défaut, fail closed.

## Partie 3 - Protocol Buffers

Avantages: encodage compact, validation intégrée, versioning natif.

Comparaison:
- JSON: 142 octets
- Protobuf: 52 octets
- Ratio: 2.7x plus petit

## Partie 4 - Politique de sérialisation

Règles:
1. Interdire pickle pour entrées non fiables
2. Utiliser JSON ou Protobuf
3. Signer avec HMAC
4. Fail closed

## Conclusion

Points clés: JSON lisible mais validation manuelle, Protobuf plus compact, pickle dangereux.