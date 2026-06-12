#  Sistema de Votação Distribuída (Python + JavaScript)

Este é um sistema de votação assíncrono e de alta disponibilidade construído para demonstrar conceitos práticos de **Arquitetura de Sistemas Distribuídos**. O objetivo do projeto é criar uma estrutura totalmente desacoplada onde o envio do voto é feito de forma instantânea para o utilizador, delegando o processamento pesado e o armazenamento para serviços independentes em segundo plano.

---

##  Como o Projeto Funciona

O fluxo de funcionamento do sistema foi desenhado para suportar múltiplos acessos simultâneos sem sobrecarregar o servidor principal, operando através dos seguintes passos:

1. **Interface de Votação (Frontend):** O utilizador acede a uma página web responsiva (otimizada para computadores e telemóveis) e escolhe a sua tecnologia favorita (Python ou JavaScript). Ao clicar, um script assíncrono (`Fetch API`) envia o voto para o servidor.

2. **Recebimento Instantâneo (API Gateway):** A API desenvolvida em **FastAPI** recebe a requisição do voto e, em vez de perder tempo a salvar diretamente na base de dados, ela simplesmente coloca o voto dentro de uma fila de mensagens e responde imediatamente `200 OK` para o utilizador. Isso faz com que a interface seja extremamente rápida.

3. **Garantia de Entrega (RabbitMQ):** O **RabbitMQ** atua como o Broker de mensagens (mensageria). Ele recebe os votos enviados pela API e os organiza em uma fila segura. Mesmo que o sistema receba milhares de votos por segundo, o RabbitMQ armazena-os em um "buffer" para garantir que nenhum voto seja perdido.

4. **Processamento em Segundo Plano (Worker):** Um script Python independente (Worker) fica escutando a fila do RabbitMQ em tempo real. Assim que um novo voto entra na fila, o Worker consome essa mensagem, processa o dado e faz o incremento de forma segura.

5. **Armazenamento e Leitura Rápida (Redis):** O Worker salva o placar final dentro do **Redis**, que é um banco de dados em memória de altíssima velocidade. Quando a página web precisa de exibir os resultados atualizados, a API busca os números diretamente do cache do Redis, garantindo uma resposta instantânea na tela.

6. **Acesso Externo via QR Code:**
   Através de um túnel seguro criado com o **ngrok**, o sistema gera um endereço público na internet. Esse link é convertido em um **QR Code** exibido diretamente na tela do sistema, permitindo que qualquer pessoa aponte a câmara do telemóvel e vote de fora da rede local.