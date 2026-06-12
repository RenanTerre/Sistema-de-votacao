import pika
import json
import time
import redis

# Configurações locais (de acordo com as constants)
RABBITMQ_HOST = "localhost"
QUEUE_NAME = "fila_votos"
REDIS_HOST = "localhost"
REDIS_PORT = 6379

# Conecta direto ao Redis aqui para garantir que o worker seja independente
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def callback(ch, method, properties, body):
    try:
        dados = json.loads(body)
        opcao = dados["opcao"]
        
        # Incrementa o voto no Redis de forma atômica
        chave = f"votos_{opcao}"
        novo_total = redis_client.incr(chave)
        
        print(f" [x] Voto para '{opcao}' processado com sucesso! Novo total: {novo_total}")
        
        # Confirma para o RabbitMQ que a mensagem foi processada
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f" [!] Erro ao processar mensagem: {e}")

def iniciar_worker():
    print(' [*] Aguardando conexão com RabbitMQ...')
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            break
        except Exception:
            print(" [...] RabbitMQ ainda não está pronto, tentando novamente em 3 segundos...")
            time.sleep(3)

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    print(' [*] Worker ativo e escutando a fila. Para sair pressione CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    iniciar_worker()