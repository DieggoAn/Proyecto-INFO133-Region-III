from typing import TextIO
#import chanarcilloNews  #Cuando se ejecuta main.py , ejecuta chanarcilloNews.py
import mysql.connector
#Formato para la fecha / insertRow-insertManyRow
"""
https://codigolinea.com/insertando-fechas-con-diferente-formato-en-mysql/
https://www.youtube.com/watch?v=ju-toIbHk_4
https://www.w3schools.com/python/python_mysql_insert.asp
"""
#newsChanarcillo = searchItem()
#dataChanarcillo = chanarcilloNews.formatDB(newslist)
#for i in newsChanarcillo:
#    print(i,"")

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
#
#"""       Formato de ingreso para InsertRow
  url   = 'https://www.chanarcillo.cl/instituto-de-investigacion-de-ciencias-sociales-y-educacion-de-la-universidad-de-atacama-culmina-ciclo-de-seminarios/'
  titulo= 'Instituto de Investigación de Ciencias Sociales y Educación de la Universidad de Atacama culmina ciclo de seminarios'
  fecha = '2022-07-13'
  Texto = 'Esto sera un exito txt '

val = (url, titulo, Texto,fecha)
#InsertRow(val)

#"""



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
def InsertManyRow(streamersList): #Insertar multiples-filas en formato lista de *(tupla,)*    
  cursor = mydb.cursor()
  try: 
      sql = f"INSERT INTO NOTICIA (URL_NOTICIA, TITULO, TEXTO, FECHA_PUB) VALUES (?, ?, ?, ?)"
      cursor.executemany(sql, streamersList)
  except mysql.Error as e: 
      print(f"Error: {e}")
  commit(cursor)

#
##--------------------FIN DE Funciones -------------------

##--------------------ejecutar Funciones-------------------

InsertRow(val)

