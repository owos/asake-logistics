# Chatbot Hogwarts :speech_balloon:
## Informações
- Autor : João Paulo Wakugawa 
- API : <a href="http://hp-api.herokuapp.com/">Harry-Potter</a>
- Link do Okteto : <a href="https://web-jpwakugawa.cloud.okteto.net/">Chat de Hogwarts</a>

---

## Funcionamento
O chatbot recepciona o usuário em Hogwarts e oferece um tour pela escola, o usúario pode escolher a entre as casas Grifinória, Sonserina, Corvinal e Lufa-lufa, feito isso o bot seleciona um personagem aleátorio da casa escolhida para acompanhar o convidado, também é possível vizualizar o histórico dos personagens que acompanharam os convidados.

---

# Desenvolvimento :red_circle:
## Actions 
### action_show_character 
Responsável por selectionar um personagem aleátorio da api, mostrar o personagem e guardá-lo no banco de dados.
### action_show_history 
Responsável por mostrar todos os personagem que foram armazenados no banco de dados. 

---

## Utilizando o Rasa
```
$ rasa init            // Criando uma pasta com config iniciais
$ rasa train           // Treinando o modelo
    --fixed-model-name // Flag para gerar modelo com nome específico
$ rasa run actions     // Lembrar de reiniciar sempre que houver alterações
$ rasa shell           // Testando as funcionalidades do modelo
    -vv                // Flag para mostrar mais detalhes
$ rasa interactive     // Auxilia na definição de uma story 
```

## Utilizando o Webchat
```
$ rasa run actions                   // Servidor responsável pelas actions
$ rasa run --enable-api --cors="*"   // Liberando comunicação entre os servidores
$ python3 -m http.server             // Servidor Front-end
```
## Utilizando o Docker
O bot-3 realiza a integração do bot-2 em docker, subindo a aplicação em 4 partes:
- Rasa
- Actions
- Web 
- Ngrok
```
$ docker-compose up // Subindo a aplicação localmente
```

## Utilizando o Okteto
- A aplicacão pode ser acessada através do <a href="">Okteto</a>.
```
$ okteto stack deploy --build // Buildando do docker-compose
```

---

## Tecnologias e depêndencias :books:
- <a href="https://rasa.com/docs/rasa/installation/">Rasa</a>
- <a href="https://docs.python.org/3/">Python</a>
- <a href="https://docs.mongodb.com/">MongoDB</a>
- <a href="https://pymongo.readthedocs.io/en/stable/index.html">Pymongo</a>
- <a href="https://github.com/scalableminds/chatroom">Chatroom</a>
- <a href="https://docs.docker.com/">Docker</a>
- <a href="https://okteto.com/docs/getting-started/index.html">Okteto</a>
