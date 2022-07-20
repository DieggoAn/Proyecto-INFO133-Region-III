from requests_html import HTMLSession
from AGENT import USER_AGENT
import dateutil.parser as parser
randAgent = USER_AGENT()


def formatoDate(dateRaw):
    dateRaw = dateRaw.split(" ")
    m = {
        'enero,': "01",'febrero,': "02",'marzo,': "03",'abril,': "04",
        'mayo,': "05",'junio,': "06",'julio,': "07",'agosto,': "08",
        'septiembre,': "09",'octubre,': "10",'noviembre,': "11",'diciembre,': "12"
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
            title = newsitem.text
            link  = newsitem.absolute_links
            newstime = item.find('time', first=True)
            formatLink = ",".join(link)
            noticia = noticiaText(formatLink)
            newstime = item.find('time', first=True)
            fecha    = formatoDate(newstime.text)
            listRaw.append(tuple((formatLink, title,noticia,fecha,'https://www.nostalgica.cl/')))
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