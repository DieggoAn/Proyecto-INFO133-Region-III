# importing required libraries
import mysql.connector
 
dataBase = mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd ="5284",
  database = "Atacama"
)
 
# preparing a cursor object
cursorObject = dataBase.cursor()

# creating table 
Noticia = """CREATE TABLE IF NOT EXISTS NOTICIA (
                   Titulo  text NOT NULL,
                   Fecha Date,
                   URLs VARCHAR(512),
                   Texto text NOT NULL
                   )"""
Medio = """CREATE TABLE IF NOT EXISTS MEDIO(
                    Nombres VARCHAR(50),
                    URLs VARCHAR(512),
                    Tipo VARCHAR(10),
                    Region INT,
                    Pais VARCHAR(20),
                    Fecha Date 
                    )"""         
Duenho = """CREATE TABLE IF NOT EXISTS DUENHO(
                    Nombre VARCHAR(50),
                    Tipo VARCHAR(10),
                    Fecha Date
                     )"""          
Mencion = """CREATE TABLE IF NOT EXISTS MENCION(
                    Nombre  VARCHAR(50),
                    Wiki VARCHAR(512),
                    Profesion VARCHAR(30),
                    Fecha Date,
                    Nacionalidad VARCHAR(20)    
                    )"""
Popularidad = """CREATE TABLE IF NOT EXISTS POPULARIDAD(
                    Fecha date,
                    Valor INT
                    )"""
 

cursorObject.execute(Noticia)
cursorObject.execute(Medio)
cursorObject.execute(Duenho)
cursorObject.execute(Mencion)
cursorObject.execute(Popularidad)

# cursorObject.execute("SHOW DATABASES")
