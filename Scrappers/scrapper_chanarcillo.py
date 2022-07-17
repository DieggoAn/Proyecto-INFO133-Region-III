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
    numPag = 1
    url = 'https://www.chanarcillo.cl/category/region-actualidad/page/'+str(numPag)+'/'

    r = session.get(url,headers=headers)
    articles = r.html.find('article')

    listRaw   = []
    for item in articles:
        try:
            newsitem = item.find('h2', first=True) 
            title   = newsitem.text
            link    = newsitem.absolute_links
            formatLink = ",".join(link)
            noticia = noticiaText(formatLink)
            newstime = item.find('time', first=True)
            fecha    = formatoDate(newstime.text)
            listRaw.append(tuple((formatLink, title, noticia, fecha)))
        except Exception as e:
            print("Error:", e)
    return listRaw

#Funcion que Rescata toda la noticia y la retorna en formato str
def noticiaText(direccion):
    r2 = session.get(direccion,headers=headers)
    selector = '.entry-content'
    ubicacion = r2.html.find(selector)
    segmentNew = []
    try:
        for item in ubicacion:
            newsitem = item.find('p') 
        for i in newsitem:
            segmentNew.append(i.text)
    except Exception as e:
        pass
    allNew = '\n'.join(segmentNew)  
    return allNew


def main():
    links    = searchItem()                  #Recolecta los link con su (titulos, texto, fecha)
    ##----------------------IMPRIME EN CONSOLA -> LAS NOTICIAS <- -------------------
    c=0
    for i in links:
        c+=1
        print("----------------->",c,"<-------------------------")
        print(i,"")
    ##------------------------- FIN CODIGO ------------------------
#
main()