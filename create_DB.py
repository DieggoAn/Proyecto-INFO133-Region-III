import mysql.connector



#in_host = input("Host: ")
in_user = input("Usuario: ")
in_passwd = input("Contraseña: ")

dataBase = mysql.connector.connect(
  host = "localhost",
  user = in_user,
  passwd = in_passwd,
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE IF NOT EXISTS Atacama")

cursorObject.execute(dataBase.close())

dataBase = mysql.connector.connect(
  host = "localhost",
  user = in_user,
  passwd = in_passwd,
  database = "Atacama",
)

cursorObject = dataBase.cursor()

# Tablas Simples
Dueno = """CREATE TABLE IF NOT EXISTS DUENO(
        ID_DUENO INT PRIMARY KEY,
        NOMBRE VARCHAR(50),
        TIPO VARCHAR(10)
        )"""

Medio = """CREATE TABLE IF NOT EXISTS MEDIO(
        URL_MEDIO VARCHAR(512) PRIMARY KEY,
        NOMBRE VARCHAR(50),
        PAIS VARCHAR(20),
        IDIOMA VARCHAR(20),
        REGION TINYINT,
        FECHA_CRE DATE
        )"""

Persona = """CREATE TABLE IF NOT EXISTS PERSONA(
        ID_PERSONA INT PRIMARY KEY,
        WIKI VARCHAR(512),
        NOMBRE VARCHAR(50),
        PROFESION VARCHAR(50),
        NACIONALIDAD VARCHAR(20),
        FECHA_NAC DATE
        )"""

Popularidad = """CREATE TABLE IF NOT EXISTS POPULARIDAD(
        FECHA_POP DATE PRIMARY KEY
        )"""

# Tablas Dependientes
Noticia = """CREATE TABLE IF NOT EXISTS NOTICIA(
        URL_NOTICIA VARCHAR(512) PRIMARY KEY,
        TITULO VARCHAR(512),
        TEXTO TEXT NOT NULL,
        FECHA_PUB DATE,
        URL_MEDIO VARCHAR(512),
        FOREIGN KEY (URL_MEDIO) REFERENCES MEDIO (URL_MEDIO)
        )""" 

# Tablas Intermedias
Adquiere = """CREATE TABLE IF NOT EXISTS ADQUIERE(
        ID_DUENO INT,
        FOREIGN KEY (ID_DUENO) REFERENCES DUENO (ID_DUENO),
        URL_MEDIO VARCHAR(512),
        FOREIGN KEY (URL_MEDIO) REFERENCES MEDIO (URL_MEDIO),
        FECHA_ADQ DATE
        )"""

Menciona = """CREATE TABLE IF NOT EXISTS MENCIONA(
        ID_PERSONA INT,
        FOREIGN KEY (ID_PERSONA) REFERENCES PERSONA (ID_PERSONA),
        URL_NOTICIA VARCHAR(512),
        FOREIGN KEY (URL_NOTICIA) REFERENCES NOTICIA (URL_NOTICIA)
        )"""  

Tiene = """CREATE TABLE IF NOT EXISTS TIENE(
        ID_PERSONA INT,
        FOREIGN KEY (ID_PERSONA) REFERENCES PERSONA (ID_PERSONA),
        FECHA_POP DATE,
        FOREIGN KEY (FECHA_POP) REFERENCES POPULARIDAD (FECHA_POP),
        VALOR INT
        )"""

# Tablas Simples
cursorObject.execute(Dueno)
cursorObject.execute(Medio)
cursorObject.execute(Persona)
cursorObject.execute(Popularidad)
# Tablas Dependientes
cursorObject.execute(Noticia)
# Tablas Intermedias
cursorObject.execute(Adquiere)
cursorObject.execute(Menciona)
cursorObject.execute(Tiene)

def commit(cursor):    ## make the changes
  dataBase.commit()
  print(f"Last Inserted ID: {cursor.lastrowid}")
  dataBase.close()
#
def InsertManyRow(dataInsert): #Insertar multiples-filas en formato lista de *(tupla,)*    
  cursor = dataBase.cursor()
  try: 
    sql = "INSERT IGNORE INTO MEDIO (URL_MEDIO, NOMBRE, PAIS, IDIOMA, REGION, FECHA_CRE) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, dataInsert)
  except Exception as e: 
    print(f"Error: {e}")
  commit(cursor)

#
##--------------------FIN DE Funciones -------------------
val = [
  ('https://www.redatacama.com/', 'Red Atacama', 'Chile','Español',3,'1999-08-10'),
  ('https://www.radiogennesis.cl/', 'Radio Gennesis', 'Chile','Español',3,'1998-08-03'),
  ('https://www.elquehaydecierto.cl/', 'Que Hay de Cierto', 'Chile','Español',3,'1973-09-11'),
  ('https://www.digitalfm.cl/', 'Radio Digital FM', 'Chile','Español',3,'1962-04-27'),
  ('https://www.chanarcillo.cl/', 'Diario Chañarcillo', 'Chile','Español',3,'1988-02-10'),
  ('https://www.soychile.cl/copiapo/', 'Soy Copiapo', 'Chile','Español',3,'2005-11-09'), 
  ('http://www.atacamaenlinea.cl/', 'Atacama en Linea', 'Chile','Español',3,'1987-12-31'), 
  ('https://tierramarillano.cl/', 'Tierramarillano', 'Chile','Español',3,'2009-03-19'), 
  ('https://www.nostalgica.cl/', 'Nostalgica', 'Chile','Español',3,'2004-02-21'),
  ('https://www.maray.cl/', 'Maray', 'Chile','Español',3,'2014-06-30')
]
##--------------------Persona Falsa--------------------------##
# se usar para probar scripts requests.py y extract_persons
persona = 'INSERT IGNORE INTO PERSONA(ID_PERSONA, WIKI, NOMBRE, PROFESION, NACIONALIDAD, FECHA_NAC) VALUES(1,"https://es.wikipedia.org/wiki/Gabriel_Boric","Gabriel Boric","Presidente de la Republica","Chilena","1986-02-11")'
cursorObject.execute('INSERT IGNORE INTO POPULARIDAD(FECHA_POP)VALUES("2022-07-01")')
cursorObject.execute('INSERT IGNORE INTO POPULARIDAD(FECHA_POP)VALUES("2022-06-01")')
cursorObject.execute('INSERT IGNORE INTO POPULARIDAD(FECHA_POP)VALUES("2022-05-01")')
cursorObject.execute('INSERT IGNORE INTO MEDIO(URL_MEDIO,NOMBRE,PAIS,IDIOMA,REGION,FECHA_CRE)VALUES("www.mediodeprueba.com/","Medio de prueba","Chile","Español",3,"2022-06-19")')
cursorObject.execute('INSERT IGNORE INTO NOTICIA (URL_NOTICIA,TITULO,TEXTO,FECHA_PUB,URL_MEDIO) VALUES("www.mediodeprueba.com/noticias/noticiaFalsa","Noticia falsa de prueba","A punto de cumplir 36 años, edad que lo habilita para sentarse en el Palacio de La Moneda a partir del 11 de marzo, Gabriel Boric Font fuma un cigarrillo tras otro a pocas horas de dar a conocer su gabinete.","2022,07-19","www.mediodeprueba.com/")')
cursorObject.execute('INSERT IGNORE INTO MENCIONA (ID_PERSONA, URL_NOTICIA) VALUES (1,"www.mediodeprueba.com/noticias/noticiaFalsa")')
cursorObject.execute(persona) 



InsertManyRow(val) 