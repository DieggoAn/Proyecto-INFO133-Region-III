import mysql.connector

#in_host = input("Host: ")
in_user = input("Usuario: ")
in_passwd = input("Contraseña: ")

dataBase = mysql.connector.connect(
  host = "localhost",
  user = in_user,
  passwd = in_passwd,
  database = "Atacama"
)

# Definir objeto cursos
cursorObject = dataBase.cursor(buffered=True)

##contador noticias por medio
cursorObject.execute("SELECT URL_MEDIO, count(URL_MEDIO) from noticia group by URL_MEDIO;") 
print("Cuantas noticias ha publicado cada medio: ")
print(str(cursorObject.fetchall()))
print()

##Persona mencionada en una noticia en un dia especifico //Modificar valor de FECHA_PUB
cursorObject.execute("SELECT NOMBRE, FECHA_PUB FROM persona p JOIN menciona m ON p.ID_PERSONA = m.ID_PERSONA JOIN noticia n ON m.URL_NOTICIA = n.URL_NOTICIA WHERE FECHA_PUB = '2022-07-19';")
print("Personas mencionadas en una fecha especifica: ")
print(str(cursorObject.fetchall()))
print()

##Evolucion de popularidad de una persona, cambiar ID_PERSONA="x" para ver otra persona de la base de datos##
cursorObject.execute('SELECT ID_PERSONA, VALOR from tiene where ID_PERSONA="1"')

Lista_POP = list(cursorObject.fetchall())

d1 = [item[1] for item in Lista_POP]
if d1[-1] < d1[-2]:
  print ("Comparacion Popularidad mes actual con mes anterior: -", round(100 - (d1[-1]/d1[-2])*100)," %")
elif  d1[-1]==d1[-2]:
  print ("Comparacion Popularidad mes actual con mes anterior: +0 %")
else:
  print ("Comparacion Popularidad mes actual con mes anterior: +",round (((d1[-1]/d1[-2])*100)-100)," %")
print(Lista_POP)
print()

##5 medios de prensa mas antiguos de una region 
cursorObject.execute("SELECT NOMBRE, FECHA_CRE FROM medio WHERE REGION = '3' ORDER BY FECHA_CRE ASC LIMIT 5;")
print("5 medios de prensa mas antiguos de una region: ")
print(str(cursorObject.fetchall()))
