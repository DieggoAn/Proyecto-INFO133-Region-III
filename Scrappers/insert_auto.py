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
    sql = "INSERT INTO NOTICIA (URL_NOTICIA, TITULO, TEXTO, FECHA_PUB) VALUES (%s, %s, %s, %s)"
    cursor.executemany(sql, dataInsert)
  except mysql.Error as e: 
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
