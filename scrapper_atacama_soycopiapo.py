from requests_html import HTMLSession
import random

URL_MEDIO = "https://www.soychile.cl/copiapo"
XPATH_URLS = "//h2[@class='media-heading']//a//@href"

XPATH_DATE = "//span[@class='media-fecha-modificacion']"
XPATH_TITLE = "//h1[@class='note-inner-title']//puskeleton"
XPATH_TEXT = "//div[@class='note-inner-text']"

def formatWait(xpath_text):
  texto = xpath_text
  texto = texto.replace("/","").replace("@","")
  c = 0
  while texto[c] != "]":
    c += 1
  return texto[0:c+1]

WAIT_URLS = formatWait(XPATH_URLS)
WAIT_DATE = formatWait(XPATH_DATE)
WAIT_TITLE = formatWait(XPATH_TITLE)
WAIT_TEXT = formatWait(XPATH_TEXT)

INTENTOS = 5

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

async def funcionUrls(url_medio):
  global list_href
  list_href = []
  print("Scrapeando Noticias en: \"", url_medio,"\"")
  await respuesta.html.page.waitForSelector(WAIT_URLS)
  page_urls = await respuesta.html.page.xpath(XPATH_URLS)
  for i in range(0,len(page_urls)):
    text_url = await respuesta.html.page.evaluate('(e) => e.textContent', page_urls[i])
    if "/copiapo" in text_url:
      list_href.append(text_url)
  await respuesta.html.page.close()
  print("Listo...")

async def funcionNoticia(url_noticia):
  global text_fecha
  global text_title
  global text_text
  print("Scrapeando \"", url_noticia,"\"")
  await respuesta.html.page.waitForSelector(WAIT_DATE)
  page_fecha = await respuesta.html.page.xpath(XPATH_DATE)
  text_fecha = await respuesta.html.page.evaluate('(e) => e.textContent', page_fecha[0])
  page_title = await respuesta.html.page.xpath(XPATH_TITLE)
  text_title = await respuesta.html.page.evaluate('(e) => e.textContent', page_title[0])
  page_text = await respuesta.html.page.xpath(XPATH_TEXT)
  text_text = await respuesta.html.page.evaluate('(e) => e.textContent', page_text[0])
  await respuesta.html.page.close()
  print("Listo...")

def renderizar_pagina(url_pagina):
  global respuesta
  respuesta = sesionHTML.get(url_pagina,headers=headers)
  intentos = INTENTOS
  while intentos > 0:
    try:
      print("Renderizando:", url_pagina)
      respuesta.html.render(sleep=1,keep_page=True)
      print("Renderizado Existoso...")
    except Exception as e:
      print("Error de Renderizado:", e)
    else:
      intentos = 1
    intentos -= 1

def scraping_soycopiapo():
  global sesionHTML
  sesionHTML = HTMLSession()
  renderizar_pagina(URL_MEDIO)
  sesionHTML.loop.run_until_complete(funcionUrls(URL_MEDIO))
  for href in list_href:
    url_noticia = URL_MEDIO[:23] + href
    renderizar_pagina(url_noticia)
    sesionHTML.loop.run_until_complete(funcionNoticia(url_noticia))
  sesionHTML.close()

def scraping_data():
  global sesionHTML
  dicc_info = {}
  sesionHTML = HTMLSession()
  renderizar_pagina(URL_MEDIO)
  sesionHTML.loop.run_until_complete(funcionUrls(URL_MEDIO))
  c = 0
  for href in list_href:
    url_noticia = URL_MEDIO[:23] + href
    renderizar_pagina(url_noticia)
    sesionHTML.loop.run_until_complete(funcionNoticia(url_noticia))
    dicc_info["Obj" + str(c)] = {"text":text_text,"title":text_title,"date":text_fecha}
    c += 1
    if c == 2:
      break
  sesionHTML.close()
  return dicc_info

#Esta es la funcion que ejecuta lo pedido
#scraping_soycopiapo()