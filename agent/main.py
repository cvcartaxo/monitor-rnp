import time
import schedule
from monitor import NetworkMonitor
from database import InfluxDBClient
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MonitoringAgent:
    def __init__(self):
        self.monitor = NetworkMonitor()
        self.db = InfluxDBClient()
        
    def run_tests(self):
        """Executa todos os testes de monitoramento"""
        try:
            logger.info("Iniciando ciclo de monitoramento")
            
            # Teste de Ping
            ping_results = self.monitor.ping_test("8.8.8.8")
            self.db.write_ping_data(ping_results)
            
            # Testes de Sites
            sites = ["google.com", "youtube.com", "rnp.br"]
            for site in sites:
                web_results = self.monitor.website_test(site)
                self.db.write_web_data(web_results)
                
            logger.info("Ciclo de monitoramento concluído")
            
        except Exception as e:
            logger.error(f"Erro no ciclo de monitoramento: {e}")
    
    def start(self):
        """Inicia o agente de monitoramento"""
        logger.info("Agente de monitoramento iniciado")
        
        # Executa a cada 1 minuto
        schedule.every(1).minutes.do(self.run_tests)
        
        # Executa imediatamente ao iniciar
        self.run_tests()
        
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    agent = MonitoringAgent()
    agent.start()