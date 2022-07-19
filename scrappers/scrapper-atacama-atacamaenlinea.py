from requests_html import HTMLSession
from AGENT import USER_AGENT
global session
global headers
#= Agentes de usuario para ingresar a una pagina sin ser identificado como un bot
randAgent = USER_AGENT()

#= Solicitar estructura web
session = HTMLSession()
headers = {'user-agent':randAgent }
##
def searchItem():    

    url = 'http://www.atacamaenlinea.cl/'
    r = session.get(url,headers=headers)

    articles = r.html.find('article')
    ##
    formatForDB = []
    for item in articles: 
        try:
            newsitem    = item.find('h4', first=True) 
            title       = newsitem.text
            link        = newsitem.absolute_links
            formatLink  = ",".join(link)
            noticia = noticiaText(formatLink,'.inner-entry-content')
            newsfecha    = item.find('.posts-date', first=True) 

            fecha = newsfecha.text      #   FALTA FORMATEAR LA FECHA <-------------------------------------------

            formatForDB.append(tuple((formatLink,title, noticia,fecha)))
        except Exception as e:
            pass
            print(f"Error>:",e)
    return formatForDB
##
##
def noticiaText(direccion,selector):
    r2 = session.get(direccion,headers=headers)
    ubicacion = r2.html.find(selector)
    try:
        for item in ubicacion:
            return item.text
    except Exception as e:
        print(f"Error>:",e)
##
##
def main():
    formatForDB    = searchItem()                  #Recolecta los link con su (titulos, texto, fecha)
    ##----------------------IMPRIME EN CONSOLA -> LAS NOTICIAS <- -------------------
    c=0
    for i in formatForDB:
        c+=1
        print("----------------->",c,"<-------------------------")
        print(i,"")
    ##----------------------
#
main()

#noticiaText('http://www.atacamaenlinea.cl/participacion-femenina-en-las-empresas-un-eje-prioritario/columnas/','.inner-entry-content')