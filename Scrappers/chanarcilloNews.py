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
    numPag = 2
    #url = 'https://www.chanarcillo.cl/category/region-actualidad/page/1/'
    url = 'https://www.chanarcillo.cl/category/region-actualidad/page/'+str(numPag)+'/'

    r = session.get(url,headers=headers)
    articles = r.html.find('article')

    listRaw   = []
    for item in articles:
        try:
            newsitem = item.find('h2', first=True) 
            title   = newsitem.text
            link    = newsitem.absolute_links
            formato = ",".join(link)
            noticia = noticiaText(formato)
            newstime = item.find('time', first=True)
            fecha    = formatoDate(newstime.text)
            listRaw.append(tuple((link, title, fecha, noticia)))
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

##Funcion que agrega la noticia a la Lista de Url, title, date
## Funcion que por el link toma la noticia y la guarda en la lista Noticia

def listDataNews(dataWithLink):
    dataWithNew = []
    for i in dataWithLink:
        aux = noticiaText(','.join(i[0]))
        dataWithNew.append(aux)
    return dataWithNew

def createTupleForDB(dataWithLink,dataWithNew):
    numNew = 0
    dataForDB = []
    for i in dataWithLink:
        formato = ",".join(i[0])
        dataForDB.append(tuple((formato,i[1],dataWithNew[numNew],i[2])))
        numNew+= 1
    
    return dataForDB

def formatDB():
    links    = searchItem()                 
    news    = listDataNews(links)           
    dataForDB = createTupleForDB(links,news)
    return dataForDB

def main():
    links    = searchItem()                  #Recolecta los link
    #news    = listDataNews(links)           #con los link recolecta las noticias
    #dataForDB = createTupleForDB(links) #Une todo en una lista de tupla en formato:
                                             #(link, title,texto,fecha ) listo para ingresar DB
    #links.clear()
    #news.clear()

    ##----------------------IMPRIME EN CONSOLA -> LAS NOTICIAS <- -------------------
    c=0
    for i in links:
        c+=1
        print("----------------->",c,"<-------------------------")
        print(i,"")
    ##------------------------- FIN CODIGO ------------------------
#main()