import mysql.connector
 
dataBase = mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd ="5284",
  database = "Atacama"
)

# Definir objeto cursos
cursorObject = dataBase.cursor()
baseMedio = "INSERT INTO  MEDIO (URL_MEDIO_PK, NOMBRE, PAIS, IDIOMA, REGION, FECHA_CRE) VALUES ('http://www.diarioatacama.cl', 'El diario de Atacama', 'Chile', 'Espanol', 'Atacama', '1970-08-01')"


cursorObject.execute(baseMedio)
                 
       