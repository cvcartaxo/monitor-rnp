import requests
import time
from ping3 import ping
import logging

logger = logging.getLogger(__name__)

class NetworkMonitor:
    def __init__(self):
        self.timeout = 10
        
    def ping_test(self, host):
        """Teste de ping com latência e perda de pacotes"""
        try:
            latency = ping(host, timeout=self.timeout)
            
            if latency is None or latency is False:
                return {
                    "host": host,
                    "latency_ms": None,
                    "packet_loss": 100,
                    "status": "failed"
                }
            
            return {
                "host": host,
                "latency_ms": round(latency * 1000, 2),
                "packet_loss": 0,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Erro no ping test para {host}: {e}")
            return {
                "host": host,
                "latency_ms": None,
                "packet_loss": 100,
                "status": "error"
            }
    
    def website_test(self, url):
        """Teste de tempo de carregamento e status code"""
        start_time = time.time()
        
        try:
            # Adiciona protocolo se não existir
            if not url.startswith(('http://', 'https://')):
                url = f'https://{url}'
            
            response = requests.get(url, timeout=self.timeout, allow_redirects=True)
            load_time = round((time.time() - start_time) * 1000, 2)
            
            return {
                "website": url,
                "load_time_ms": load_time,
                "status_code": response.status_code,
                "status": "success" if response.status_code == 200 else "warning"
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro no website test para {url}: {e}")
            return {
                "website": url,
                "load_time_ms": None,
                "status_code": None,
                "status": "error"
            }