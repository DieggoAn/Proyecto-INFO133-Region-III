from requests_html import HTMLSession
import random
import mysql.connector

#=====================[0]CONSTANTES[0]]=====================#
#= Para Medio:"diarioatacama" URL:"https://www.soychile.cl/copiapo/"
#= (Cuidado de diferenciar "Soycopiapo" con "Soychile")
XPATH_DATE = "//span[@class='media-fecha-modificacion']"
XPATH_TITLE = "//h1[@class='note-inner-title']//puskeleton"
XPATH_TEXT = "//div[@class='note-inner-text']"

#= | //div[@class=''] | -----> | div[class=''] |
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

#= Imprimir las constantes luego del formatWait
#= print(WAIT_DATE,WAIT_TEXT,WAIT_TITLE)

#= Agentes de usuario para ingresar a una pagina sin ser identificado como un bot
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

#=====================[O]LISTA DE NOTICIAS[O]=====================#
#= (¡¡IMPORTANTE!! la url de las noticias debe de coincidir con la
#= clave primaria "URL_MEDIO" en la tabla MEDIO esto para que el codigo
#= pueda ingresar la clave fornea "URL_MEDIO" en la tabla NOTICIA)
#=
#= Puede ser un upgrade interesante implementar alguna solucion
#= Queda en espera hasta afinar detalles
#=====================[X]LISTA DE NOTICIAS[X]]=====================#
doc = ["http://www.soychile.cl/copiapo/policial/2022/06/30/764289/detienen-a-mujer-por-crimen.html","http://www.soychile.cl/copiapo/sociedad/2022/06/29/764119/tasa-desempleo-en-atacama.html","http://www.soychile.cl/copiapo/sociedad/2022/06/28/763909/uda-realiza-especializacion-ginecologia.html","http://www.soychile.cl/copiapo/policial/2022/06/26/763729/persona-resulta-herida-a-bala.html","http://www.soychile.cl/copiapo/sociedad/2022/06/25/763638/ceaza-pronostica-lluvias-en-atacama.html","http://www.soychile.cl/copiapo/policial/2022/06/24/763537/formalizan-a-sujeto-por-homicidio.html","http://www.soychile.cl/copiapo/policial/2022/06/23/763412/detienen-a-asaltantes-de-servicentro.html","http://www.soychile.cl/copiapo/sociedad/2022/06/23/763329/huasco-comienza-celebracion-san-pedro.html","http://www.soychile.cl/copiapo/sociedad/2022/06/22/763093/sorpresiva-lluvia-en-copiapo.html","http://www.soychile.cl/copiapo/policial/2022/06/21/763038/recuperan-vehiculo-robado-tierra-amarilla.html","http://www.soychile.cl/copiapo/sociedad/2022/06/21/763034/casos-diarios-covid-atacama.html","http://www.soychile.cl/copiapo/policial/2022/06/21/763033/arresto-de-adolescentes.html","http://www.soychile.cl/copiapo/sociedad/2022/06/19/762752/casos-diarios-covid-atacama.html","http://www.soychile.cl/copiapo/policial/2022/06/19/762748/choque-al-poste-en-huasco.html","http://www.soychile.cl/copiapo/sociedad/2022/06/19/762744/rescate-en-parque-tres-cruces.html","http://www.soychile.cl/copiapo/policial/2022/06/17/762478/adolescente-muerto-en-copiapo.html","http://www.soychile.cl/copiapo/sociedad/2022/06/16/762286/diputada-cid-rechaza-asesinato.html","http://www.soychile.cl/copiapo/policial/2022/06/15/762115/atacama-con-378-casos-covid.html","http://www.soychile.cl/copiapo/policial/2022/06/14/761935/formalizan-a-chofer-accidente-palomar.html","http://www.soychile.cl/copiapo/sociedad/2022/06/28/763906/pescadores-se-toman-ruta.html"]

#= URL a escrapear
URL = doc[4]

#=====================[X]CONSTANTES[X]]=====================#

#=====================[O]FUNCIONES DE FORMATO[O]=====================#
#= # Las funciones de formato tienen como objetivo manejar la informacion
#= directamente salida del scraping y modificar las cadenas de texto para
#= poder ser añadidas a traves de SQL sin tener problemas de formato.
#====================================================================#
#= Esta funcion tranforma la cadena extraida del scraping
#= de un origen de la forma "DD de MONTH de YYYY | hh:mm"
#= y lo tranforma a la forma "YYYY-MM-DD"
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

#=======================================================#
#= Esta funcion quita espacios en blanco que quedan
#= en la cadena del titulo extraida del scraping
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

#=====================[X]FUNCIONES DE FORMATO[X]=====================#

#===========================[O]SCRAP[O]===========================#
#= #Se optó por hacer las peticiones en la misma funcion "async",
#= a pesar de no ser necesario el JavaScript con algunos
#= atributos y no ser la forma mas eficiente.
#= Aporta un standar seguro con la informacion concentrada
#= y versatilidad a la hora de editar, corregir y manejar el codigo.
#===========================[X]SCRAP[X]===========================#

#==========[O]FUNCION PARA ACCEDER AL JS DE LA PAGINA[O]==========#
async def funcionJs():
  global norm_fecha
  global norm_title
  global norm_text

#= Esperar la respuesta hasta que cargue la etiqueta WAIT seleccionada
  await response.html.page.waitForSelector(WAIT_DATE)

#= Extraer fecha
  page_fecha = await response.html.page.xpath(XPATH_DATE)
  text_fecha = await response.html.page.evaluate('(e) => e.textContent', page_fecha[0])
  norm_fecha = format_date(text_fecha)

#= Extraer titulo
  page_title = await response.html.page.xpath(XPATH_TITLE)
  text_title = await response.html.page.evaluate('(e) => e.textContent', page_title[0])
  norm_title = format_title(text_title)

#= Extraer texto
  page_text = await response.html.page.xpath(XPATH_TEXT)
  text_text = await response.html.page.evaluate('(e) => e.textContent', page_text[0])
  norm_text = text_text

#==========[X]FUNCION PARA ACCEDER AL JS DE LA PAGINA[X]==========#

#=======================================================#
#= Solicitar estructura web
headers = {'user-agent':random.choice(USER_AGENT_LIST) }
session = HTMLSession()
response = session.get(URL,headers=headers)

response.html.render(sleep=1,keep_page=True)

#=======================================================#
# Conectarse a MariaDB para guardar los datos escrapeados
inputUserOn = True
while inputUserOn:
  in_user = input("Usuario: ")
  in_passwd = input("Contraseña: ")
  try:
    dataBase = mysql.connector.connect(
    host = "localhost",
    user = in_user,
    passwd = in_passwd,
    database = "atacama")
  except Exception as e:
    print("Hubo un error en la conexion a MariaDB:", e)
  else:
    inputUserOn = False

# Get Cursor
cursorObject = dataBase.cursor(buffered=True)

#Ejecutar el Scraping
try:
  session.loop.run_until_complete(funcionJs())
finally:
  cursorObject.execute("SELECT URL_MEDIO FROM MEDIO;")
  ###### FUNCION BUSCAR URL_MEDIO ######
  medios = []
  for i in cursorObject:
    medios.append(i[0])
  for i in medios:
    if i in URL:
      url_medio = i
  ######################################
  print(URL)
  print(norm_fecha)
  print(norm_title)
  print(norm_text)
  cursorObject.execute(f"INSERT INTO noticia (URL_NOTICIA,TITULO,TEXTO,FECHA_PUB,URL_MEDIO) VALUES ('{URL}', '{norm_title}', '{norm_text}', '{norm_fecha}', '{url_medio}')")
  dataBase.commit() #Guardar los datos en MariaDB
  dataBase.close()

  #= Existe un problema para cerrar, a veces, de forma aleatoria, no te permite cerrar la sesion
  #= No supone un riesgo para la funcionalidad, quedese libre se ser corregido o no
  session.close()