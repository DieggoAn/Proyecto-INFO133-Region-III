from typing import TextIO
import mysql.connector
## INICIO MEDIOS
import atacama_chanarcillo  #Cuando se ejecuta main.py , ejecuta .chanarcilloNews.py
import atacama_atacamaenlinea
import atacama_tamarillano
import atacama_nostalgia
#
import  atacama_soycopiapo
import atacama_digitalfm2
## FIN MEDIOS

##
##---------------------->Inicio Scraping <--------------------------------
print("Start Scraping...")
##
dataChanarcillo = atacama_chanarcillo.searchItem()
print("Ready Chanarcillo . . .",len(dataChanarcillo))
##
dataAtacamaenlinea = atacama_atacamaenlinea.searchItem() 
print("Ready AtacamaOnline . . .",len(dataAtacamaenlinea))
##
datatamarillano = atacama_tamarillano.searchItem() 
print("Ready Tamarillo . . .",len(datatamarillano))
##
##
dataNostalgia = atacama_nostalgia.searchItem() 
print("Ready Nostalgia . . .",len(dataNostalgia))
#
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
    sql = "INSERT IGNORE INTO NOTICIA (URL_NOTICIA, TITULO, TEXTO, FECHA_PUB) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, row)
  except mysql.Error as e: 
      print(f"Error: {e}")
  commit(cursor)
#
def insertManyRow(dataInsert): #Insertar multiples-filas en formato lista de *(tupla,)*    
  global cursor
  cursor = mydb.cursor()
  try: 
    sql = "INSERT IGNORE INTO NOTICIA (URL_NOTICIA, TITULO, TEXTO, FECHA_PUB) VALUES (%s, %s, %s, %s)"
    cursor.executemany(sql, dataInsert)
  except Exception as e: 
    print(f"Error: {e}")

#
val = [
  ('https://www.redatacama.com/', 'Red Atacama', 'Chile','Español',3,'1999-08-10'),
  ('https://www.radiogennesis.cl/', 'Radio Gennesis', 'Chile','Español',3,'1998-08-03'),
  ('https://www.elquehaydecierto.cl/', 'Que Hay de Cierto', 'Chile','Español',3,'1973-09-11'),
  ('https://www.digitalfm.cl/', 'Radio Digital FM', 'Chile','Español',3,'1962-04-27'),
  ('https://www.chanarcillo.cl/', 'Diario Chañarcillo', 'Chile','Español',3,'1988-02-10'),
  ('https://www.soychile.cl/copiapo/', 'Soy Copiapo', 'Chile','Español',3,'2005-11-09'), 
  #('https://www.redatacama.com/', 'Red Atacama', 'Chile','Español',3,'2011-10-25'),
  #('https://www.redatacama.com/', 'Red Atacama', 'Chile','Español',3,'1873-01-18'),
]

def insertMedio(dataInsert): #Insertar multiples-filas en formato lista de *(tupla,)*    
  global cursor
  cursor = mydb.cursor()
  try: 
    sql = "INSERT INTO MEDIO (URL_MEDIO, NOMBRE, PAIS,IDIOMA,REGION, FECHA_CRE) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, dataInsert)
  except Exception as e: 
    print(f"Error: {e}")
##
def autoDB():
  #insertMedio(val)
  #print("Ready MEDIOS on MariaDB")

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
      data = atacama_soycopiapo2.scraper()
    elif i[0] == 'https://www.elquehaydecierto.cl/':
      data = ata.scraper()
    elif i[0] == 'https://www.digitalfm.cl/':
      data = atacama_digitalfm2.scraper()
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


