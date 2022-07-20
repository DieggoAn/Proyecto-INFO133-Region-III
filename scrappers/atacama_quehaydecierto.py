from requests_html import HTMLSession
import random

def formatWait(xpath_text):
  texto = xpath_text
  texto = texto.replace("/","").replace("@","")
  c = 0
  while texto[c] != "]":
    c += 1
  return texto[0:c+1]
from requests_html import HTMLSession

URL_MEDIO = "https://www.elquehaydecierto.cl/bien-comun"
XPATH_URLS = "//div[@class='pensando-txt']//h4//a//@href"

XPATH_DATE = "//div[@class='date-created-node']//span"
XPATH_TITLE = "//h1[@class='page-header']"
XPATH_TEXT = "//div[@class='content content-node']//p"

WAIT_URLS = "div[class='pensando-txt']"
WAIT_NEWS = "div[class='date-created-node']"

USER_AGENT = {'user-agent':"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"}

INTENTOS = 5

session = HTMLSession()

async def extraer_xpaths(wait,*args):
  datos = []
  c = 1
  while c <= INTENTOS:
    try:
      print("Esperando Selector:", wait)
      await respuesta.html.page.waitForSelector(wait)
    except Exception as e:
      print("[Intento: {}] Espera Fallida:".format(c), e)
      c += 1
    else:
      print("Listo...")
      break
  for arg in args:
    raw_xpath = await respuesta.html.page.xpath(arg)
    for i in range(len(raw_xpath)):
      text_xpath = await respuesta.html.page.evaluate('(e) => e.textContent', raw_xpath[i])
      datos.append(text_xpath)
  await respuesta.html.page.close()
  return datos

def renderizar(sleep_time,pagina):
  global respuesta
  respuesta = session.get(pagina,headers=USER_AGENT)
  c = 1
  while c <= INTENTOS:
    try:
      print("Renderizando", pagina)
      respuesta.html.render(sleep=sleep_time,keep_page=True)
    except Exception as e:
      print("[Intento: {}] Error de Renderizado:".format(c), e)
      c += 1
    else:
      print("Renderizado Exitoso...")
      return
  print("Se omite el scraping de", pagina)

def extraer_urls():
  renderizar(2,URL_MEDIO)
  return session.loop.run_until_complete(extraer_xpaths(WAIT_URLS,XPATH_URLS)) 

def scraper():
  hrefs = extraer_urls()
  datos_tupla = []
  for href in hrefs:
    url = URL_MEDIO[:31] + href
    renderizar(0,url)
    ttf = session.loop.run_until_complete(extraer_xpaths(WAIT_NEWS,XPATH_TITLE,XPATH_TEXT,XPATH_DATE))
    datos_tupla.append(tuple((url, ttf[0], ttf[1], ttf[2])))
  return datos_tupla

def scrap_text():
  hrefs = extraer_urls()
  textos = []
  for href in hrefs:
    url = URL_MEDIO[:31] + href
    renderizar(0,url)
    ttf = session.loop.run_until_complete(extraer_xpaths(WAIT_NEWS,XPATH_TEXT))
    textos.append(ttf[0])
  return textos