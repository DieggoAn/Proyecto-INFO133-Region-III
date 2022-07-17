from operator import contains
from requests_html import HTMLSession
from AGENT import USER_AGENT
from requests import session
##
##
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
    #
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
            if(c == 1 ):
                #FALTA EXTRAER LA NOTICIA POR EL SELECTOR QUE CORRESPONDE
                #noticia = noticiaText2(formatLink,'.entry-content')
                noticia = "Eurecaaaa"  
            else:                
                noticia = noticiaText(formatLink)
            print("Noticia numero ----------------->>>",c,"<<<--------------------------------------")     
            print(formatLink)
            print(noticia)
            #newslist.append(tuple((formatLink,title,fecha)))
            c+=1
        except Exception as e:
            print(f"Error>:",e)
    return newslist
##
##
#Funcion que Rescata toda la noticia y la retorna en formato str
def noticiaText(direccion):
    r2 = session.get(direccion,headers=headers)
    selector = '.elementor-widget-container'
    ubicacion = r2.html.find(selector)
    try:
        segmentNew  =   ubicacion[10].text
        return segmentNew
    except Exception as e:
        print(f"Error>:",e)
    
def noticiaText2(direccion,selector):
    r2 = session.get(direccion,headers=headers)
    ubicacion = r2.html.find(selector)
    try:
        segmentNew  =   ubicacion[10].text
        allNew = '\n'.join(segmentNew)  
        return segmentNew
    except Exception as e:
        print(f"Error>:",e)
##
##
def printCMD(data):
    c=1
    for i in data:
        print("Noticia numero ----------------->>>",c,"<<<--------------------------------------")     
        print(i[0],i[1],i[2])
        c+=1


searchItem()
#printCMD(data)

