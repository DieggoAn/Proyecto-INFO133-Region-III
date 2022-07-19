from requests_html import HTMLSession
from AGENT import USER_AGENT
from requests import session


#= Agentes de usuario para ingresar a una pagina sin ser identificado como un bot
randAgent = USER_AGENT()


#= Solicitar estructura web
headers = {'user-agent':randAgent }
session = HTMLSession()

#url = 'https://www.chanarcillo.cl/region-de-atacama-se-confirma-la-llegada-de-un-nuevo-sistema-frontal/'
url = 'https://www.chanarcillo.cl/rocio-diaz-seremi-de-vivienda-y-urbanismo-tenemos-los-recursos-para-poder-lograr-la-meta-de-construir-7-500-viviendas-en-4-anos-para-enfrentar-el-deficit/'
r = session.get(url,headers=headers)
print("",url,"")

articles = r.html.find('article')

newslist = []

for item in articles: 
    try:
        newsitem = item.find('h1', first=True) 
        newstime = item.find('time', first=True)
        newsText = item.find('p', first=True)
        fecha    = newstime.text
        title    = newsitem.text
        texto    = newsText.text
        newslist.append(tuple((title,texto, fecha)))
    except:
        pass

# Imprime la lista con informacion    
print(len(newslist))
for i in newslist:
    print(i)
    print("")