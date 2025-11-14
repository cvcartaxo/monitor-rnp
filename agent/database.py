from influxdb_client import InfluxDBClient as InfluxClient
from influxdb_client.client.write_api import SYNCHRONOUS
import os

class InfluxDBClient:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'influxdb')
        self.port = os.getenv('DB_PORT', '8086')
        self.token = "my-super-secret-token"
        self.org = "monitoring-org"
        self.bucket = "monitoring"
        
        self.client = InfluxClient(
            url=f"http://{self.host}:{self.port}",
            token=self.token,
            org=self.org
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
    
    def write_ping_data(self, data):
        """Escreve dados de ping no InfluxDB"""
        from influxdb_client import Point
        
        point = Point("ping_metrics")\
            .tag("host", data["host"])\
            .tag("status", data["status"])\
            .field("latency_ms", data["latency_ms"] or 0)\
            .field("packet_loss", data["packet_loss"])
            
        self.write_api.write(bucket=self.bucket, record=point)
    
    def write_web_data(self, data):
        """Escreve dados web no InfluxDB"""
        from influxdb_client import Point
        
        point = Point("web_metrics")\
            .tag("website", data["website"])\
            .tag("status", data["status"])\
            .field("load_time_ms", data["load_time_ms"] or 0)\
            .field("status_code", data["status_code"] or 0)
            
        self.write_api.write(bucket=self.bucket, record=point)