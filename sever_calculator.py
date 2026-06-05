import Pyro5.api
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


@Pyro5.api.expose
class CalculatorService:
    """Service de calcul exposé comme objet distant"""
    
    def add(self, a: float, b: float) -> float:
        """Additionne deux nombres"""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise ValueError("Les arguments doivent être des nombres")
        
        result = a + b
        logger.info(f"add({a}, {b}) = {result}")
        return result
    
    def subtract(self, a: float, b: float) -> float:
        """Soustrait deux nombres"""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise ValueError("Les arguments doivent être des nombres")
        
        result = a - b
        logger.info(f"subtract({a}, {b}) = {result}")
        return result
    
    def multiply(self, a: float, b: float) -> float:
        """Multiplie deux nombres"""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise ValueError("Les arguments doivent être des nombres")
        
        result = a * b
        logger.info(f"multiply({a}, {b}) = {result}")
        return result
    
    def divide(self, a: float, b: float) -> float:
        """Divise deux nombres"""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise ValueError("Les arguments doivent être des nombres")
        if b == 0:
            raise ValueError("Division par zéro impossible")
        
        result = a / b
        logger.info(f"divide({a}, {b}) = {result}")
        return result
    
    def _internal_reset(self):
        """Méthode INTERNE - NON exposée à distance"""
        logger.warning("Méthode _internal_reset appelée (ne devrait pas être accessible)")
        pass


def main():
    """Démarre le serveur CalculatorService"""
    with Pyro5.api.Daemon() as daemon:
        # Localiser le name server
        try:
            ns = Pyro5.api.locate_ns()
            logger.info("Name Server trouvé")
        except Exception as e:
            logger.error(f"Impossible de contacter le Name Server: {e}")
            logger.error("Assurez-vous que 'python -m Pyro5.nameserver' est en cours d'exécution")
            return
        
        # Enregistrer l'objet
        uri = daemon.register(CalculatorService)
        ns.register("example.calculator", uri)
        
        logger.info(f"CalculatorService prêt")
        logger.info(f"URI: {uri}")
        logger.info("Appuyez sur Ctrl+C pour arrêter")
        
        daemon.requestLoop()


if __name__ == "__main__":
    main()