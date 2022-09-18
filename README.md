# Hogwarts Chatbot :speech_balloon:
 ## Information
 - Author : 
 - API : 
 ---

 ## Operation
 The chatbot is for logistics.
 ---

 # Development :red_circle:
 ## Actions
 ### action_show_character
 Responsible for selecting a random character from the api, showing the character and saving it in the database.
 ### action_show_history
 Responsible for showing all characters that were stored in the database.

 ---

 ## Using Rasa
 ```
 $ rasa init // Creating a folder with initial config
 $ rasa train // Training the model
     --fixed-model-name // Flag to generate model with specific name
 $ rasa run actions // Remember to restart whenever there are changes
 $ rasa shell // Testing model functionality
     -vv // Flag to show more details
 $ rasa interactive // ​​Helps in defining a story
 ```

 ## Using Webchat
 ```
 $ rasa run actions // Server responsible for actions
 $ rasa run --enable-api --cors="*" // Enabling communication between servers
 $ python3 -m http.server // Server Frontend
 ```
 ## Using Docker
 Bot-3 performs the integration of bot-2 in docker, uploading the application in 4 parts:
 - Shallow
 - Actions
 - Web
 - Ngrok
 ```
 $ docker-compose up // Uploading the application locally
 ```

 ## Using Okteto
 - The application can be accessed through <a href="">Okteto</a>.
 ```
 $ okteto stack deploy --build // Building from docker-compose
 ```

 ---

 ## Technologies and dependencies :books:
 - <a href="https://rasa.com/docs/rasa/installation/">Rasa</a>
 - <a href="https://docs.python.org/3/">Python</a>
 - <a href="https://docs.mongodb.com/">MongoDB</a>
 - <a href="https://pymongo.readthedocs.io/en/stable/index.html">Pymongo</a>
 - <a href="https://github.com/scalableminds/chatroom">Chatroom</a>
 - <a href="https://docs.docker.com/">Docker</a>
 - <a href="https://okteto.com/docs/getting-started/index.html">Okteto</a>
