import random
from requests import head, session
from requests_html import HTMLSession

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

#= Solicitar estructura web
headers = {'user-agent':random.choice(USER_AGENT_LIST) }
session = HTMLSession()

url = 'https://www.chanarcillo.cl/category/region-actualidad/'

r = session.get(url,headers=headers)

articles = r.html.find('article')

##Listas con data
newslist            = []        # Contiene ->   Title , link , fecha
newslistNoticias    = []        # contiene ->   Texto (del link superior)
dataForDB           = []

##Por modificar para agregar mas parrafos a textoNews

def noticiaText(direccion, agente):
    session2 = HTMLSession()
    headers = {'user-agent':random.choice(agente) }
    r2 = session2.get(direccion,headers=headers)
    articles = r2.html.find('article')
    for items in articles:
        try:
            newsitem = items.find('p', first=True) 
            textoNews   = newsitem.text
            return textoNews
        except:
            pass


def noticiaText(direccion, agente):
    session2 = HTMLSession()
    headers = {'user-agent':random.choice(agente) }
    r2 = session2.get(direccion,headers=headers)


    selector = '.entry-content'
    ubicacion = r2.html.find(selector)
    segmentNew = []

    for item in ubicacion:
        newsitem = item.find('p') 

    for i in newsitem:
        segmentNew.append(i.text)
    allNew = '\n'.join(segmentNew)  

    return allNew

def searchItem():
    for item in articles: 
        try:
            newsitem = item.find('h2', first=True) 
            title   = newsitem.text
            link    = newsitem.absolute_links
            newstime = item.find('time', first=True)
            fecha    = newstime.text
            """
            noticia = noticiaText(link, USER_AGENT_LIST)
            print(noticia)
            """
            dataForDB.append(list((title, link, fecha )))
        except:
            pass
    return dataForDB

## IMPRIME LAS NOTICIAS
def printNews(dataForDB,indice):
    for i in dataForDB:
        print("-------------NOTICIA-Numero",indice,"---------------------")
        print("                 URL")
        print(''.join(i[1]),"")
        print("                 PORTADA")
        print(''.join(i[0]),"")
        print("                 FECHA")
        print(''.join(i[2]),"")
        print("                 TEXTO")
        noticia = noticiaText(','.join(i[1]), USER_AGENT_LIST)
        print(noticia , "")
        indice+=1

def formatDB(dataForDB):
    for i in dataForDB:
        noticia = noticiaText(','.join(i[1]), USER_AGENT_LIST)
        i.append(noticia)
    return dataForDB


#searchItem()
#printNews(newslist,1)


#Tareas por realizar
#Inserta datos a la base de datos
# Importar base de datos main    -> CreateDB
#                                -> Insertar medio Chanarcillo
#                                -> Insertar Medio Soychile
#                                -> SELECT ... FROM ....