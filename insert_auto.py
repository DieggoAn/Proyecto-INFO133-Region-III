from typing import TextIO
import mysql.connector
## INICIO MEDIOS
import scrappers.atacama_chanarcillo  #Cuando se ejecuta main.py , ejecuta .chanarcilloNews.py
import scrappers.atacama_atacamaenlinea
import scrappers.atacama_tamarillano
import scrappers.atacama_nostalgia
##
import scrappers.atacama_redatacama 
import scrappers.atacama_maray
import scrappers.atacama_radiogenesis
##
import  scrappers.atacama_soycopiapo
import scrappers.atacama_digitalfm2
## FIN MEDIOS

##
##---------------------->Inicio Scraping <--------------------------------

print("Start Scraping...")
##
dataChanarcillo = scrappers.atacama_chanarcillo.searchItem()
print("Ready Chanarcillo . . .",len(dataChanarcillo))
##
dataAtacamaenlinea = scrappers.atacama_atacamaenlinea.searchItem() 
print("Ready AtacamaOnline . . .",len(dataAtacamaenlinea))
##
datatamarillano = scrappers.atacama_tamarillano.searchItem() 
print("Ready Tamarillo . . .",len(datatamarillano))
##
##
dataNostalgia = scrappers.atacama_nostalgia.searchItem() 
print("Ready Nostalgia . . .",len(dataNostalgia))
##
dataRedAtacama = scrappers.atacama_redatacama.scraper()
print ("Ready RedAtacama . . .",len(dataRedAtacama))
##
dataMaray = scrappers.atacama_maray.scraper()
print ("Ready Maray . . . ",len(dataMaray) )
##
dataRadioGenesis = scrappers.atacama_radiogenesis.scraper()
print ("Ready Radio Genesis . . .",len(dataRadioGenesis))
##---------------------->FIN Scraping <--------------------------------
#
##---------------------->Inicio Codigo Marco <--------------------------------
"""

data = atacama_soycopiapo2.scraper()
data = atacama_digitalfm2.scraper()
for i in data:
  print(i)
print(len(data))

#import scrappers.atacama_quehaydecierto as quehaydecierto
#import scrappers.atacama_digitalfm as digitalfm

"""
##---------------------->Fin Codigo Marco <--------------------------------


#=======================================================#
### Connect to MariaDB Platform
inputUserOn = True
while inputUserOn:
  in_user     = input("==========================================================\nUsuario    : ")
  in_passwd   = input("Contraseña : \n")
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

##----------------------INICIO ---Funciones ------------------------------------------------##
def commit(cursor):    ## make the changes
  mydb.commit()
  print(f"Last Inserted ID: {cursor.lastrowid}")
  mydb.close()
#
def insertRow(row): #Insertar 1 filas
  cursor = mydb.cursor() 
  try: 
    sql = "INSERT IGNORE INTO NOTICIA (URL_NOTICIA, TITULO, TEXTO, FECHA_PUB, URL_MEDIO) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, row)
  except mysql.Error as e: 
      print(f"Error: {e}")
  commit(cursor)
#
def insertManyRow(dataInsert): #Insertar multiples-filas en formato lista de *(tupla,)*    
  global cursor
  cursor = mydb.cursor()
  try: 
    sql = "INSERT IGNORE INTO NOTICIA (URL_NOTICIA, TITULO, TEXTO, FECHA_PUB, URL_MEDIO) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(sql, dataInsert)
  except Exception as e: 
    print(f"Error: {e}")

##
def autoDB():
  print("Ready MEDIOS on MariaDB")

  insertManyRow(dataChanarcillo)
  print("Ready Chanarcillo on MariaDB")
  #
  insertManyRow(dataAtacamaenlinea)
  print("Ready Atacamaenlinea on MariaDB")
  #
  insertManyRow(datatamarillano)  
  print("Ready Tamarillano on MariaDB")
  #
  insertManyRow(dataNostalgia)  
  print("Ready Nostalgia on MariaDB")
  #
  insertManyRow(dataRedAtacama)
  print("Ready RedAtacama on MariaDB")
  #
  insertManyRow(dataMaray)
  print("Ready Maray on MariaDB")
  #
  insertManyRow(dataRadioGenesis)
  print("Ready Radio Genesis on MariaDB")
  #Commit he ingresa los datos a la DB
  commit(cursor)

###

def InsertUrl(var_list,url):
  lista_tupla = []
  for i in var_list:
    lista_tupla.append(i + tuple((url,)))
  return lista_tupla

def funcMarcoInsert():
  cursor = mydb.cursor(buffered=True)
  cursor.execute("SELECT URL_MEDIO FROM MEDIO")
  for i in cursor:
    data = []
    if i[0] == 'https://www.soychile.cl/copiapo/':
      data = scrappers.atacama_soycopiapo2.scraper()
    elif i[0] == 'https://www.elquehaydecierto.cl/':
      data = scrappers.atacama_quehaydecierto.scraper()
    elif i[0] == 'https://www.digitalfm.cl/':
      data = scrappers.atacama_digitalfm2.scraper()
    else:
      print(i[0], "No tiene funcion de Scraping")
    if data != []:
      data = InsertUrl(data,i[0])
      insertManyRow(data)
  mydb.close()

##--------------------FIN DE Funciones ---------------------------------------------------

##------------------INICIO--EJECUTAR FUNCIONES-------------------

autoDB()

#funcMarcoInsert()


