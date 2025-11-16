# Projeto de Monitoramento — Docker + Nginx + InfluxDB + Grafana + Agente python

Este repositório contém uma stack completa para monitoramento simples **Docker Compose**, incluindo:

- **Nginx** (proxy reverso)
- **InfluxDB 2.x** (banco de métricas)
- **Agente de Monitoramento** (ping + Python + HTTP checker)
- **Grafana** (dashboard)

## 🚀 Requisitos

Antes de iniciar, certifique-se de ter instalado:

- **Docker >= 24.x**
- **Docker Compose >= 2.x**
- **Git**
- Sistema operacional Linux, macOS ou Windows (WSL2 recomendado)

---

### Execução do projeto localmente.

```bash
git clone https://github.com/seu-repo/projeto-monitoramento.git
cd projeto-monitoramento
```

#### Build do projeto sem cache.
```bash
docker-compose build --no-cache --pull

docker compose up -d
```

#### Analise dos logs do projeto.
```bash
docker-compose logs -f
```

#### Parar todos os serviços
```bash
docker-compose down
```

#### Rebuild completo
```bash
docker-compose down && docker system prune -af && docker volume prune -f
docker-compose build --no-cache && docker-compose up -d
```

## 🚀 Como Acessar a Aplicação

### 🔐 Credenciais de Acesso

**URL:**  
https://localhost  

**Usuário:**  
`admin-rnp`

**Senha:**  
`9ZdTiIlEmrKn7TG5`

---

### Importante

- O certificado SSL utilizado é **autoassinado**, portanto o navegador exibirá um aviso de segurança.  
  Basta **aceitar o risco e continuar**.
- O acesso via **HTTP (`http://localhost`)** redireciona automaticamente para **HTTPS (`https://localhost`)**.


