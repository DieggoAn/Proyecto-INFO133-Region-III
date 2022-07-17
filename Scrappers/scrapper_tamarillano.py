from operator import contains
from requests_html import HTMLSession
from AGENT import USER_AGENT
from requests import session
##
##
import dateutil.parser as parser
##

def formatoDate(dateRaw):
    date =  parser.parse(dateRaw)
    return date.isoformat()
def searchItem():
    global  session
    global  headers
    #= Agentes de usuario para ingresar a una pagina sin ser identificado como un bot
    randAgent = USER_AGENT()

    #= Solicitar estructura web
    headers = {'user-agent':randAgent }
    session = HTMLSession()    
    #
    url = 'https://tierramarillano.cl/regionales/'
    r = session.get(url,headers=headers)
    articles = r.html.find('article')
    ##
    newslist = []
    #
    c=1
    for item in articles[1:]:
        try:
            newsitem = item.find('h3', first=True) 
            title   = newsitem.text
            link    = newsitem.absolute_links
            formatLink = ",".join(link)
            fecha = formatLink[27:37]
            fecha    = formatoDate(fecha)
            if(c < 2 ):
                noticia = noticiaText(formatLink,'.entry-content',0)
            else:                
                noticia = noticiaText(formatLink,'.elementor-widget-container',10)
            
            newslist.append(tuple((formatLink,title,noticia,fecha)))
            c+=1
        except Exception as e:
            print(f"Error>:",e)
            c+=1
    return newslist
##
##
#Funcion que Rescata toda la noticia y la retorna en formato str
def noticiaText(direccion,selector,posicion):
    r2 = session.get(direccion,headers=headers)
    ubicacion = r2.html.find(selector)
    try:
        segmentNew  =   ubicacion[posicion].text
        return segmentNew
    except Exception as e:
        print(f"Error>:",e)
##
##
def printCMD(data):
    c=1
    for i in data:
        print("Noticia numero ----------------->>>",c,"<<<--------------------------------------")     
        print(i[0],i[1],i[2],i[3])
        c+=1


data = searchItem()
print(data)

