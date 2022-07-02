from requests_html import HTMLSession
import random
import mysql.connector

#===========Constantes===========#
#Para Medio:"diarioatacama" URL:"https://www.soychile.cl/copiapo/"
#(Cuidado de diferenciar "Soycopiapo" con "Soychile")
XPATH_DATE = "//span[@class='media-fecha-modificacion']"
XPATH_TITLE = "//h1[@class='note-inner-title']//puskeleton"
XPATH_TEXT = "//div[@class='note-inner-text']"

#= //div[@class='note-inner-text'] -----> div[class='']
def formatWait(xpath_text):
  texto = xpath_text
  texto = texto.replace("/","").replace("@","")
  c = 0
  while texto[c] != "]":
    c += 1
  return texto[0:c+1]

WAIT_DATE = formatWait(XPATH_DATE)
WAIT_TITLE = formatWait(XPATH_TITLE)
WAIT_TEXT = formatWait(XPATH_TEXT)

#===/\===VER CONSTANTEs===/\===#
#print(WAIT_DATE,WAIT_TEXT,WAIT_TITLE)

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

#Lista de Noticias
doc = ["https://www.soychile.cl/copiapo/policial/2022/06/30/764289/detienen-a-mujer-por-crimen.html","https://www.soychile.cl/copiapo/sociedad/2022/06/29/764119/tasa-desempleo-en-atacama.html","https://www.soychile.cl/copiapo/sociedad/2022/06/28/763909/uda-realiza-especializacion-ginecologia.html"]

## URL que escrapear
URL = doc[0]

#=====================Funciones de formato=====================#
def format_date(raw_date):
  meses = {"Enero":"01","Febrero":"02","Marzo":"03","Abril":"04","Mayo":"05","Junio":"06","Julio":"07","Agosto":"08","Septiembre":"09","Octubre":"10","Noviembre":"11","Diciembre":"12"}
  texto = ""
  for e in range(0,len(raw_date)):
    try:
      yy_date = int(raw_date[e-4:e])
    except:
      pass
    else:
      if len(str(yy_date)) == 4:
        texto += str(yy_date) + "-"
        break
  for e in meses.keys():
    if e in raw_date:
      texto += meses[e] + "-"
      break
  for e in range(0,len(raw_date)):
    try:
      dd_date = int(raw_date[e-2:e])
    except:
      pass
    else:
      if len(str(dd_date)) == 2:
        texto += str(dd_date)
        break
  return texto

#=============================================================#
def format_title(raw_title):
  texto = raw_title
  texto = texto[len(texto)::-1]
  caracteres = "áéíóúqwertyuiopasdfghjklñzxcvbnm¿?!¡"
  c = 0
  while texto[c].lower() not in caracteres:
    c += 1
  texto = texto[c:]
  texto = texto[len(texto)::-1]
  while texto[c].lower() not in caracteres:
    c += 1
  return texto[c:]

#===================[SCRAP]===================#
#= #Se optó por hacer todas las peticiones en la misma funcion,
#= a pesar de no ser necesario el JavaScript con algunos atributos
#= y no ser lo mas eficiente, porque, aporta un standar seguro
#= a la hora de extraer etiquetas y versatilidad a la
#= hora de editar, teniendo solo 1 metodologia lo que permite
#= una mayor facilidad de correcion y edicion.
#===================[SCRAP]===================#
async def funcionJs():
  global norm_fecha
  global norm_title
  global norm_text
  #Esperar la respuesta hasta que apareza la etiqueta
  await response.html.page.waitForSelector(WAIT_DATE)
  #Extraer fecha
  page_fecha = await response.html.page.xpath(XPATH_DATE)
  text_fecha = await response.html.page.evaluate('(e) => e.textContent', page_fecha[0])
  norm_fecha = format_date(text_fecha)
  #Extraer titulo
  page_title = await response.html.page.xpath(XPATH_TITLE)
  text_title = await response.html.page.evaluate('(e) => e.textContent', page_title[0])
  norm_title =format_title(text_title)
  #Extraer texto
  page_text = await response.html.page.xpath(XPATH_TEXT)
  text_text = await response.html.page.evaluate('(e) => e.textContent', page_text[0])
  norm_text = text_text

#=======================================================#

#Solicitar Request_Html
headers = {'user-agent':random.choice(USER_AGENT_LIST) }
session = HTMLSession()
response = session.get(URL,headers=headers)

response.html.render(sleep=1,keep_page=True)

#=================Extraer url del medio=================#
c = 0
while URL[c-4:c] == "cl/h" or URL[c-5:c] == ".com/" or URL[c-4:c] == "apo/":
  c += 1
url_medio = URL[:c]
#=======================================================#

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

try:
  session.loop.run_until_complete(funcionJs())
finally: #Guardar los datos en MariaDB
  print(url_medio)
  print(URL)
  print(norm_fecha)
  print(norm_title)
  print(norm_text)
  query= f"INSERT INTO noticia (URL_NOTICIA,TITULO,TEXTO,FECHA_PUB,URL_MEDIO) VALUES ('{URL}', '{norm_title}', '{norm_text}', '{norm_fecha}', '{url_medio}')"
  cursorObject.execute(query)
  dataBase.commit()
  dataBase.close()