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
    sql = "INSERT INTO MEDIO (URL_MEDIO, NOMBRE, PAIS, IDIOMA, REGION, FECHA_CRE) VALUES (%s, %s, %s, %s, %s, %s)"
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
  #('https://www.redatacama.com/', 'Red Atacama', 'Chile','Español',3,'2011-10-25'),
  #('https://www.redatacama.com/', 'Red Atacama', 'Chile','Español',3,'1873-01-18'),
]

InsertManyRow(val) 