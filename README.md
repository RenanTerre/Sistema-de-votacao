# Sistema de Votação Distribuída

Projeto de computação distribuída utilizando **FastAPI** no backend, **RabbitMQ** como mensageria assíncrona, **Redis** para armazenamento atômico em cache e um frontend responsivo com suporte a votação via QR Code.

## Como Executar o Projeto

1. Suba os containers do Docker (Redis e RabbitMQ):
   ```bash
   docker compose up -d