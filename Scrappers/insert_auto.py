from typing import TextIO
import chanarcillo_atacama  #Cuando se ejecuta main.py , ejecuta .chanarcilloNews.py
import mysql.connector

dataChanarcillo = chanarcillo_atacama.searchItem()

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
def InsertRow(row): #Insertar 1 filas
  cursor = mydb.cursor() 
  try: 
    sql = "INSERT INTO NOTICIA (URL_NOTICIA, TITULO, TEXTO, FECHA_PUB) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, row)
  except mysql.Error as e: 
      print(f"Error: {e}")
  commit(cursor)
#
def InsertManyRow(dataInsert): #Insertar multiples-filas en formato lista de *(tupla,)*    
  cursor = mydb.cursor()
  try: 
    sql = "INSERT INTO NOTICIA (URL_NOTICIA, TITULO, TEXTO, FECHA_PUB) VALUES (%s, %s, %s, %s)"
    cursor.executemany(sql, dataInsert)
  except mysql.Error as e: 
    print(f"Error: {e}")
  commit(cursor)

#
##--------------------FIN DE Funciones -------------------

##------------------INICIO--Ejecutar Funciones-------------------

#InsertRow(test)            #Inserta 1 filas
InsertManyRow(dataChanarcillo)

