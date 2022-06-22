import mysql.connector
 
dataBase = mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd ="5284",
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE IF NOT EXISTS Atacama")

cursorObject.execute(dataBase.close())

dataBase = mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd ="5284",
  database = "Atacama",
)

cursorObject = dataBase.cursor()

# Tablas Simples
Dueno = """CREATE TABLE IF NOT EXISTS DUENO(
        ID_DUENO_PK INT PRIMARY KEY,
        NOMBRE VARCHAR(50),
        TIPO VARCHAR(10)
        )"""

Medio = """CREATE TABLE IF NOT EXISTS MEDIO(
        URL_MEDIO_PK VARCHAR(512) PRIMARY KEY,
        NOMBRE VARCHAR(50),
        PAIS VARCHAR(20),
        IDIOMA VARCHAR(20),
        REGION TINYINT,
        FECHA_CRE DATE
        )"""

Persona = """CREATE TABLE IF NOT EXISTS PERSONA(
        ID_PERSONA_PK INT PRIMARY KEY,
        POPULARIDAD INT,
        WIKI VARCHAR(512),
        NOMBRE VARCHAR(50),
        PROFESION VARCHAR(50),
        NACIONALIDAD VARCHAR(20),
        FECHA_NAC DATE
        )"""

# Tablas Dependientes
Noticia = """CREATE TABLE IF NOT EXISTS NOTICIA(
        URL_NOTICIA_PK VARCHAR(512) PRIMARY KEY,
        TITULO VARCHAR(512),
        TEXTO TEXT NOT NULL,
        FECHA_PUB DATE,
        URL_MEDIO_FK VARCHAR(512) REFERENCES MEDIO (URL_MEDIO_PK)
        )""" 

# Tablas Intermedias
Adquiere = """CREATE TABLE IF NOT EXISTS ADQUIERE(
        ID_DUENO_FK INT REFERENCES DUENO (ID_DUENO_PK),
        URL_MEDIO_FK  VARCHAR (512) REFERENCES MEDIO (URL_MEDIO_PK),
        FECHA_ADQ DATE
        )"""

Menciona = """CREATE TABLE IF NOT EXISTS MENCIONA(
        ID_PERSONA_FK  INT REFERENCES PERSONA (ID_PERSONA_PK),
        URL_NOTICIA_FK VARCHAR(512) REFERENCES NOTICIA (URL_NOTICIA_PK)
        )"""  

Popularidad = """CREATE TABLE IF NOT EXISTS POPULARIDAD(
                    ID_PERSONA_FK INT REFERENCES PERSONA (ID_PERSONA_PK),
                    FECHA date,
                    VALOR INT
                    )"""
 

cursorObject.execute(Dueno)
cursorObject.execute(Medio)
cursorObject.execute(Persona)
cursorObject.execute(Noticia)
cursorObject.execute(Adquiere)
cursorObject.execute(Menciona)
cursorObject.execute(Popularidad)

# cursorObject.execute("SHOW DATABASES")
