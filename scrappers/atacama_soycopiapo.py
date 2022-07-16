from requests_html import HTMLSession

URL_MEDIO = "https://www.soychile.cl/copiapo"
XPATH_URLS = "//h2[@class='media-heading']//a//@href"

XPATH_DATE = "//span[@class='media-fecha-modificacion']"
XPATH_TITLE = "//h1[@class='note-inner-title']//puskeleton"
XPATH_TEXT = "//div[@class='note-inner-text']"

WAIT_URLS = "h2[class='media-heading']"
WAIT_NEWS = "span[class='media-fecha-modificacion']"

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
      for href in hrefs:
            if "/copiapo/" in href:
                  url = URL_MEDIO[:23] + href
                  renderizar(0,url)
                  ttf = session.loop.run_until_complete(extraer_xpaths(WAIT_NEWS,XPATH_TITLE,XPATH_TEXT,XPATH_DATE))
                  print("[TITULO]:", ttf[0], "\n[TEXTO]:", ttf[1], "\n[FECHA]:", ttf[2])

#scraper()

def scrap_text():
      hrefs = extraer_urls()
      textos = []
      for href in hrefs:
            if "/copiapo/" in href:
                  url = URL_MEDIO[:23] + href
                  renderizar(0,url)
                  ttf = session.loop.run_until_complete(extraer_xpaths(WAIT_NEWS,XPATH_TEXT))
                  textos.append(ttf[0])
      return textos

print(scrap_text())

