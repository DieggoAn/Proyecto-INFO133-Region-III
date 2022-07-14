#Para el scraping Tutorial -> https://www.youtube.com/watch?v=uKb9fA4gyWQ
# 1) Verificamos la pagina he inspeccionamos su html como guion 
# 2) Si tiene JS necesitamos la libraria request.html
# Existen casos donde la pagina no carga toda la informacion
# Entonces tenemos que usar la libreria para cargar y extraer los datos
# 3) Tener Ojo con el formato de la fecha (no todas las paginas tienen mismo formato ) 

from requests import session
from requests_html import HTMLSession

session = HTMLSession()
url ='https://news.google.com/topstories?hl=es-419&gl=CL&ceid=CL:es-419'

r = session.get(url)

r.html.render(sleep=1, scrolldown=0)

articles = r.html.find('article')

#print(articles) #Test de informacion que retorna
"""  Primera prueba de scraping
for item in articles: 
    try:
        newsitem = item.find('h3', first=True) #Prineros filtros
        title = newsitem.text
        link = newsitem.absolute_links
        print(title, link)
    except:
        pass
"""


## Ahora lo transformamos a diccionario
newslist = []

for item in articles: 
    try:
        newsitem = item.find('h3', first=True) #Prineros filtros
        newsarticles = {
            'title': newsitem.text,
            'link' : newsitem.absolute_links
        }
        newslist.append(newsarticles)        
    except:
        pass

print(len(newslist))
for i in newslist:
    print(" ".join(i['link']))