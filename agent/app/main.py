import time
import schedule
import logging
from monitor import NetworkMonitor
from database import InfluxDBClient  # Mantém o mesmo nome de import

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MonitoringAgent:
    def __init__(self):
        self.monitor = NetworkMonitor()
        self.db = InfluxDBClient()  # Mantém o mesmo nome
        self.setup_complete = False
        
    def setup(self):
        """Configuração inicial do agent"""
        logger.info("Iniciando setup do agente de monitoramento...")
        
        # Testar conexão com o banco
        if not self.db.test_connection():
            logger.error("Não foi possível conectar ao InfluxDB")
            return False
            
        logger.info("Conexão com InfluxDB estabelecida")
        self.setup_complete = True
        return True
        
    def run_tests(self):
        """Executa todos os testes de monitoramento"""
        if not self.setup_complete:
            logger.warning("Setup não completo, pulando ciclo de monitoramento")
            return
            
        try:
            logger.info("Iniciando ciclo de monitoramento")
            
            # Teste de Ping
            ping_targets = ["8.8.8.8", "1.1.1.1"]
            for target in ping_targets:
                ping_results = self.monitor.ping_test(target)
                self.db.write_ping_data(ping_results)
                logger.info(f"Ping test para {target}: {ping_results['status']} - {ping_results.get('latency_ms', 'N/A')}ms")
            
            # Testes de Sites
            sites = ["google.com", "youtube.com", "rnp.br"]
            for site in sites:
                web_results = self.monitor.website_test(site)
                self.db.write_web_data(web_results)
                logger.info(f"Web test para {site}: {web_results['status']} - {web_results.get('load_time_ms', 'N/A')}ms")
                
            logger.info("Ciclo de monitoramento concluído")
            
        except Exception as e:
            logger.error(f"Erro no ciclo de monitoramento: {e}")
    
    def start(self):
        """Inicia o agente de monitoramento"""
        logger.info("Iniciando agente de monitoramento...")
        
        # Tentar setup por até 2 minutos
        for i in range(12):
            if self.setup():
                break
            logger.warning(f"Tentativa {i+1}/12 de setup falhou, tentando novamente em 10s")
            time.sleep(10)
        else:
            logger.error("Não foi possível completar o setup após 12 tentativas")
            return
        
        # Agendar execução a cada 1 minuto
        schedule.every(1).minutes.do(self.run_tests)
        
        # Executar imediatamente
        self.run_tests()
        
        logger.info("Agente de monitoramento iniciado com sucesso")
        
        # Loop principal
        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Agente interrompido pelo usuário")
                self.db.close()
                break
            except Exception as e:
                logger.error(f"Erro no loop principal: {e}")
                time.sleep(10)

if __name__ == "__main__":
    agent = MonitoringAgent()
    agent.start()