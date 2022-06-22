import mysql.connector
 
dataBase = mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd ="5284",
  database = "Atacama"
)

# Definir objeto cursos
cursorObject = dataBase.cursor()
baseDueno = "INSERT IGNORE INTO  DUENO (ID_DUENO_PK, NOMBRE, TIPO) VALUES (1, 'Julio', 'Persona')"
baseMedio = "INSERT IGNORE INTO MEDIO (URL_MEDIO_PK, NOMBRE, PAIS, IDIOMA, REGION, FECHA_CRE) VALUES('www.pagina.com', 'nombre', 'Chile', 'Espanol',3, '1999-09-24')"
basePersona = "INSERT IGNORE INTO PERSONA(ID_PERSONA_PK, POPULARIDAD, WIKI, NOMBRE, PROFESION, NACIONALIDAD, FECHA_NAC) VALUES(01, 100, 'www.wikipedia.com', 'Felipe', 'Profesor', 'Chilena','1999-02-27')"
baseNoticia = "INSERT IGNORE INTO NOTICIA(URL_NOTICIA_PK, TITULO, TEXTO, FECHA_PUB, URL_MEDIO_FK) VALUES('www.otrapagina.com', 'Hola' , 'chao.','2022-06-22', 'www.pagina.com')"
baseAdquiere = "INSERT IGNORE INTO ADQUIERE(ID_DUENO_FK, URL_MEDIO_FK, FECHA_ADQ) VALUES (1,'www.pagina.com', '1930-07-19')"
baseMenciona = "INSERT IGNORE INTO MENCIONA(ID_PERSONA_FK, URL_NOTICIA_FK) VALUES (01,'www.otrapagina.com')"
basePopularidad = "INSERT IGNORE INTO POPULARIDAD(ID_PERSONA_FK, FECHA, VALOR) VALUES (01, '2022-06-22', 100)"


cursorObject.execute(baseDueno)
cursorObject.execute(baseMedio)
cursorObject.execute(basePersona)
cursorObject.execute(baseNoticia)
cursorObject.execute(baseAdquiere)
cursorObject.execute(baseMenciona)
cursorObject.execute(basePopularidad)

dataBase.commit()
                 
       