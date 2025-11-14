from influxdb_client import InfluxDBClient as InfluxClient
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import logging

logger = logging.getLogger(__name__)

class InfluxDBClient:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'influxdb')
        self.port = os.getenv('DB_PORT', '8086')
        self.token = os.getenv('INFLUXDB_TOKEN', 'my-super-secret-token')
        self.org = os.getenv('INFLUXDB_ORG', 'monitoring-org')
        self.bucket = os.getenv('INFLUXDB_BUCKET', 'monitoring')
        
        # Use InfluxClient (alias) para evitar conflito de nomes
        self.client = InfluxClient(
            url=f"http://{self.host}:{self.port}",
            token=self.token,
            org=self.org
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
    
    def write_ping_data(self, data):
        """Escreve dados de ping no InfluxDB"""
        try:
            from influxdb_client import Point
            
            point = Point("ping_metrics")\
                .tag("host", data["host"])\
                .tag("status", data["status"])\
                .field("latency_ms", data["latency_ms"] or 0)\
                .field("packet_loss", data["packet_loss"])
                
            self.write_api.write(bucket=self.bucket, record=point)
            logger.debug(f"Dados de ping salvos: {data['host']}")
            
        except Exception as e:
            logger.error(f"Erro ao escrever dados de ping: {e}")
    
    def write_web_data(self, data):
        """Escreve dados web no InfluxDB"""
        try:
            from influxdb_client import Point
            
            point = Point("web_metrics")\
                .tag("website", data["website"])\
                .tag("status", data["status"])\
                .field("load_time_ms", data["load_time_ms"] or 0)\
                .field("status_code", data["status_code"] or 0)
                
            self.write_api.write(bucket=self.bucket, record=point)
            logger.debug(f"Dados web salvos: {data['website']}")
            
        except Exception as e:
            logger.error(f"Erro ao escrever dados web: {e}")
    
    def test_connection(self):
        """Testa a conexão com o InfluxDB"""
        try:
            # Testa se consegue fazer ping na API
            health = self.client.ping()
            return health
        except Exception as e:
            logger.error(f"Teste de conexão falhou: {e}")
            return False
    
    def close(self):
        """Fecha a conexão com o InfluxDB"""
        try:
            self.client.close()
        except Exception as e:
            logger.error(f"Erro ao fechar conexão: {e}")