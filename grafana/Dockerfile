FROM grafana/grafana:latest

# Variáveis de ambiente
ENV GF_SECURITY_ADMIN_USER=admin
ENV GF_SECURITY_ADMIN_PASSWORD=admin123
ENV GF_INSTALL_PLUGINS="grafana-clock-panel,grafana-piechart-panel,grafana-worldmap-panel,btplc-status-dot-panel,volkovlabs-variable-panel"


# Copiar configurações de provisionamento
COPY provisioning /etc/grafana/provisioning

# Criar diretório para dados persistentes
VOLUME ["/var/lib/grafana"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:3000/api/health || exit 1

# Expor porta
EXPOSE 3000

# Comando padrão
CMD ["/run.sh"]