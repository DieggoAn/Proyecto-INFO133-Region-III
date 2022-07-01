import random
from requests_html import HTMLSession
from pymongo import MongoClient
import time
import mysql.connector
import json

## Simular que estamos utilizando un navegador web
USER_AGENT_LIST = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
headers = {'user-agent':random.choice(USER_AGENT_LIST) }

doc = ["https://www.soychile.cl/copiapo/policial/2022/06/30/764289/detienen-a-mujer-por-crimen.html","https://www.soychile.cl/copiapo/sociedad/2022/06/29/764119/tasa-desempleo-en-atacama.html","https://www.soychile.cl/copiapo/sociedad/2022/06/28/763909/uda-realiza-especializacion-ginecologia.html"]

## URL que escrapear
URL = doc[0]

#Conectarse a Mongo para listar las URLs que escrapear
client = MongoClient("localhost", port=27017)
db=client.atacama

# Conectarse a MariaDB para guardar los datos escrapeados
in_user = input("Usuario: ")
in_passwd = input("Contraseña: ")

dataBase = mysql.connector.connect(
  host = "localhost",
  user = in_user,
  passwd = in_passwd,
  database = "atacama"
)

# Get Cursor
cursorObject = dataBase.cursor(buffered=True)

#Listar las URLs que escrapear
#for doc in db.urls.find({"to_download":True}).limit(2):

#Solicitar Request
session = HTMLSession()
response = session.get(URL,headers=headers)

response.html.render(sleep=1)

## Analizar el contenido
print(response.content)
#print(response.html)
#print(response.content)
#print(response.html.xpath("//span[@class='media-fecha-modificacion']"))


#Extraer URL del Medio
for i in range(0,len(URL)):
  if URL[i-4:i] == ".cl/":
    url_medio = URL[0:i]
    break
  else:
    url_medio = "N/A"

print(url_medio)

#Guardar los datos en MariaDB
#query= f"INSERT INTO noticia (URL_NOTICIA,TITULO,TEXTO,FECHA_PUB,URL_MEDIO) VALUES ('{URL}', '{title}', '{text}', '{date}', '{url_medio}')"

#cursorObject.execute(query)
dataBase.commit()

dataBase.close()