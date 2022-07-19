from typing import TextIO
import atacama_chanarcillo  #Cuando se ejecuta main.py , ejecuta .chanarcilloNews.py
import atacama_atacamaenlinea
import atacama_tamarillano
import mysql.connector
print("Start Scraping...")

dataChanarcillo = atacama_chanarcillo.searchItem()
print("Ready Chanarcillo . . .")
dataAtacamaenlinea = atacama_atacamaenlinea.searchItem() 
print("Ready AtacamaOnline . . .")
datatamarillano = atacama_tamarillano.searchItem() 
print("Ready tamarillo . . .")
##---------------------->Inicio Codigo Marco <--------------------------------
import scrappers.atacama_soycopiapo as soycopiapo
import scrappers.atacama_quehaydecierto as quehaydecierto
import scrappers.atacama_digitalfm as digitalfm
##---------------------->Fin Codigo Marco <--------------------------------
#=======================================================#
### Connect to MariaDB Platform
inputUserOn = True
while inputUserOn:
  in_user     = input("Usuario    : ")
  in_passwd   = input("Contraseña : ")
  #in_user     = "admin"
  #in_passwd   = "123456789"
  try:
    mydb  = mysql.connector.connect(
      user    = in_user,
      passwd  = in_passwd,
      host    = "localhost",
      #port   = 3306,
      database = "Atacama"
    )
  except Exception as e:
    print("Hubo un error en la conexion a MariaDB:  ", e)
  else:
    inputUserOn = False

##----------------------INICIO ---Funciones ----------------
def commit(cursor):    ## make the changes
  mydb.commit()
  print(f"Last Inserted ID: {cursor.lastrowid}")
  mydb.close()
#
def insertRow(row): #Insertar 1 filas
  cursor = mydb.cursor() 
  try: 
    sql = "INSERT INTO NOTICIA (URL_NOTICIA, TITULO, TEXTO, FECHA_PUB) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, row)
  except mysql.Error as e: 
      print(f"Error: {e}")
  commit(cursor)
#
def insertManyRow(dataInsert): #Insertar multiples-filas en formato lista de *(tupla,)*    
  global cursor
  cursor = mydb.cursor()
  try: 
    sql = "INSERT INTO NOTICIA (URL_NOTICIA, TITULO, TEXTO, FECHA_PUB, URL_MEDIO) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(sql, dataInsert)
  except Exception as e: 
    print(f"Error: {e}")
  #commit(cursor)

#
def autoDB():
  cursor = mydb.cursor()
  insertManyRow(dataChanarcillo)
  print("Ready Chanarcillo on MariaDB")
  insertManyRow(dataAtacamaenlinea)
  print("Ready Atacamaenlinea on MariaDB")
  insertManyRow(datatamarillano)  
  print("Ready tamarillano on MariaDB")
  commit(cursor)


##--------------------FIN DE Funciones -------------------

##------------------INICIO--Ejecutar Funciones-------------------

autoDB()
def InsertUrl(var_list,url):
  lista_tupla = []
  for i in var_list:
    lista_tupla.append(i + tuple((url,)))
  return lista_tupla

cursor = mydb.cursor(buffered=True)
cursor.execute("SELECT URL_MEDIO FROM MEDIO")
for i in cursor:
  data = []
  if i[0] == 'https://www.soychile.cl/copiapo/':
    data = soycopiapo.scraper()
  elif i[0] == 'https://www.elquehaydecierto.cl/':
    data = quehaydecierto.scraper()
  elif i[0] == 'https://www.digitalfm.cl/':
    data = digitalfm.scraper()
  else:
    print(i[0], "No tiene funcion de Scraping")
  if data != []:
    data = InsertUrl(data,i[0])
    insertManyRow(data)
mydb.close()
