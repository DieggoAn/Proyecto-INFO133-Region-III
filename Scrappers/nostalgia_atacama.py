from hashlib import new
from more_itertools import first
from requests_html import HTMLSession
from AGENT import USER_AGENT
import dateutil.parser as parser
randAgent = USER_AGENT()


def formatoDate(dateRaw):
    date =  parser.parse(dateRaw)
    return date.isoformat()

# PRIMERA FUNCION, Busca Los h2 , link , fecha
#Retorna una tupla con los LINK, titulos y fecha en la Lista listRaw
def searchItem():
    global session
    global headers
    #= Solicitar estructura web
    headers = {'user-agent':randAgent }
    session = HTMLSession()
    url = 'https://www.nostalgica.cl/atacama/'

    r = session.get(url,headers=headers)
    articles = r.html.find('article')

    listRaw   = []
    for item in articles:
        try:
            newsitem = item.find('h2', first=True) #Primeros filtros

            title = newsitem.text,
            link  = newsitem.absolute_links
            newstime = item.find('time', first=True)
            fecha = newstime.text
            formatLink = ",".join(link)
            noticia = noticiaText(formatLink)
            newstime = item.find('time', first=True)
            #fecha    = formatoDate(newstime.text)
            listRaw.append(tuple((formatLink, title,noticia, fecha )))
        except Exception as e:
            print("Error:", e)
    return listRaw

##
def noticiaText(direccion):
    r2 = session.get(direccion,headers=headers)
    ubicacion = r2.html.find('article')
    segmentNew = []
    try:
        for item in ubicacion:
            newsitem = item.find('p')
            break
        for i in newsitem:
            segmentNew.append(i.text)
    except Exception as e:
        print("Error:", e)
    allNew = '\n'.join(segmentNew) 
    return allNew


#---------------------------------------------------
dataa = searchItem()
for i in dataa:
    print(i)
    print("")

 
"""
headers = {'user-agent':randAgent }
session = HTMLSession()

url = 'https://www.nostalgica.cl/atacama/'

r = session.get(url,headers=headers)

r.html.render(sleep=1, scrolldown=5)

articles = r.html.find('article')
newslist = []

for item in articles: 
    try:
        newsitem = item.find('h2', first=True) #Primeros filtros

        title = newsitem.text,
        link  = newsitem.absolute_links
        newstime = item.find('time', first=True)
        fecha = newstime.text
        formatLink = ",".join(link)

    
        print(formatLink, title,fecha)
    except:
        pass
"""