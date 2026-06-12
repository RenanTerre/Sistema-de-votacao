import json
import pika
import redis

# Configurações de conexão (apontando para o localhost do Docker)
REDIS_HOST = "localhost"
REDIS_PORT = 6379
RABBITMQ_HOST = "localhost"
QUEUE_NAME = "fila_votos"


class SistemaDistribuidoService:

    def __init__(self):
        # Inicializa a conexão com o Redis (Cache Distribuído)
        self.redis_client = redis.Redis(
            host=REDIS_HOST, port=REDIS_PORT, decode_responses=True
        )

    def enviar_voto_para_fila(self, opcao: str):
        """Envia a intenção de voto de forma assíncrona para a fila do RabbitMQ"""
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST)
        )
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME)

        # Cria a mensagem em formato JSON
        mensagem = json.dumps({"opcao": opcao})

        # Publica na fila do RabbitMQ
        channel.basic_publish(
            exchange="", routing_key=QUEUE_NAME, body=mensagem
        )
        connection.close()

    def obtener_placar_cache(self) -> dict:
        """Busca os resultados consolidados diretamente do Cache (Redis)"""
        votos_python = self.redis_client.get("votos_python") or 0

        # Busca os votos para JavaScript, garantindo que seja um inteiro mesmo que a chave não exista
        votos_js = self.redis_client.get("votos_javascript") or 0

        return {"python": int(votos_python), "javascript": int(votos_js)}

    def incrementar_voto_no_redis(self, opcao: str) -> int:
        """Método atômico usado pelo Worker para atualizar o contador no Redis"""
        chave = f"votos_{opcao}"
        return self.redis_client.incr(chave)