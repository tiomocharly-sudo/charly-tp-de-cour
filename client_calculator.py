#!/usr/bin/env python3
"""Client CalculatorService - Consomme le service distant"""

import Pyro5.api
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Client de démonstration"""
    try:
        # Localiser le name server
        ns = Pyro5.api.locate_ns()
        
        # Récupérer l'URI du service
        uri = ns.lookup("example.calculator")
        logger.info(f"Service trouvé: {uri}")
        
        # Créer le proxy
        with Pyro5.api.Proxy(uri) as calc:
            # Tester les opérations
            print("\n" + "="*50)
            print("CALCULATOR SERVICE - TESTS")
            print("="*50)
            
            # Addition
            result = calc.add(10, 5)
            print(f"10 + 5 = {result}")
            
            # Soustraction
            result = calc.subtract(10, 3)
            print(f"10 - 3 = {result}")
            
            # Multiplication
            result = calc.multiply(7, 6)
            print(f"7 × 6 = {result}")
            
            # Division
            result = calc.divide(15, 3)
            print(f"15 ÷ 3 = {result}")
            
            # Test gestion d'erreur
            print("\n--- Tests des cas d'erreur ---")
            try:
                calc.divide(10, 0)
            except Exception as e:
                print(f"Division par zéro: {e}")
            
            try:
                calc.add("10", 5)  # Type invalide
            except Exception as e:
                print(f"Type invalide: {e}")
                
    except Pyro5.errors.NamingError:
        logger.error("Service 'example.calculator' non trouvé")
        logger.error("Assurez-vous que le serveur est démarré")
    except Exception as e:
        logger.error(f"Erreur: {e}")


if __name__ == "__main__":
    main()