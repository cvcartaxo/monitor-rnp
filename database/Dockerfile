FROM influxdb:2.7-alpine

# Variáveis de ambiente para configuração automática
ENV DOCKER_INFLUXDB_INIT_MODE=setup
ENV DOCKER_INFLUXDB_INIT_USERNAME=admin
ENV DOCKER_INFLUXDB_INIT_PASSWORD=password123
ENV DOCKER_INFLUXDB_INIT_ORG=monitoring-org
ENV DOCKER_INFLUXDB_INIT_BUCKET=monitoring
ENV DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=my-super-secret-token

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8086/ping || exit 1

# Expor porta
EXPOSE 8086

# Comando padrão (já vem no image oficial)
CMD ["influxd"]