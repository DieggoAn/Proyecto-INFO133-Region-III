from typing import TextIO
import scrappers.chanarcilloNews  #Cuando se ejecuta main.py , ejecuta scrappers.chanarcilloNews.py
import mysql.connector
#Formato para la fecha / insertRow-insertManyRow
"""
https://codigolinea.com/insertando-fechas-con-diferente-formato-en-mysql/
https://www.youtube.com/watch?v=ju-toIbHk_4
https://www.w3schools.com/python/python_mysql_insert.asp
"""

dataChanarcillo = scrappers.chanarcilloNews.formatDB()

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
"""       Formato de ingreso para InsertRow
  url   = 'https://www.chanarcillo.cl/instituto-de-investigacion-de-ciencias-sociales-y-educacion-de-la-universidad-de-atacama-culmina-ciclo-de-seminarios/'
  titulo= 'Instituto de Investigación de Ciencias Sociales y Educación de la Universidad de Atacama culmina ciclo de seminarios'
  fecha = '2022-07-13'
  Texto = 'Esto sera un exito txt '

val = (url, titulo, Texto,fecha)
#InsertRow(val)

"""

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
val = [
  ('Peter', 'Lowstreet 4',      'Lowstreet 4', '2022-07-13'),
  ('Amy', 'Apple st 652',       'Lowstreet 4', '2022-07-13'),
  ('Hannah', 'Mountain 21',     'Lowstreet 4', '2022-07-13'),
  ('Michael', 'Valley 345',     'Lowstreet 4', '2022-07-13'),
  ('Sandy', 'Ocean blvd 2',     'Lowstreet 4', '2022-07-13'),
  ('Betty', 'Green Grass 1',    'Lowstreet 4', '2022-07-13'),
  ('Richard', 'Sky st 331',    'Lowstreet 4', '2022-07-13'),
  ('Susan', 'One way 98',       'Lowstreet 4', '2022-07-13'),
  ('Vicky', 'Yellow Garden 2',  'Lowstreet 4', '2022-07-13'),
  ('Ben', 'Park Lane 38',       'Lowstreet 4', '2022-07-13'),
  ('William', 'Central st 954', 'Lowstreet 4', '2022-07-13'),
  ('Chuck', 'Main Road 989',    'Lowstreet 4', '2022-07-13'),
  ('Viola', 'Sideway 1633',     'Lowstreet 4', '2022-07-13')
]
##--------------------ejecutar Funciones-------------------
#InsertManyRow(val)             ##Test Formato y insertar multiples funciones
InsertManyRow(dataChanarcillo)

