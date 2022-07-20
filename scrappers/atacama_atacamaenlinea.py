from requests_html import HTMLSession
from AGENT import USER_AGENT
import dateutil.parser as parser
##
##s
global session
global headers
#= Agentes de usuario para ingresar a una pagina sin ser identificado como un bot
randAgent = USER_AGENT()

#= Solicitar estructura web
session = HTMLSession()
headers = {'user-agent':randAgent }
##
##
#months = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
#day =   dateRaw[:2]
#mes =   dateRaw[6:11]
#year=   dateRaw[15:]
    
##  

def formatoDate(dateRaw):
    dateRaw = dateRaw.split(" de ")
    m = {
        'enero': "01",'febrero': "02",'marzo': "03",'abril': "04",
        'mayo': "05",'junio': "06",'julio': "07",'agosto': "08",
        'septiembre': "09",'octubre': "10",'noviembre': "11",'diciembre': "12"
    }
    dia =  dateRaw[0]
    mes =  dateRaw[1]
    anio = dateRaw[2]
    try:
        out = str(m[mes.lower()])
        date = str(anio+"/"+out+"/"+dia)
        return date
    except:
        raise ValueError('No es un mes')
    
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

            #fecha = newsfecha.text      #   FALTA FORMATEAR LA FECHA <-------------------------------------------
            fecha = formatoDate(newsfecha.text)
            formatForDB.append(tuple((formatLink,title, noticia,fecha, 'http://www.atacamaenlinea.cl/')))
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
#main()