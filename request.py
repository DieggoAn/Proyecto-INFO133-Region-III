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
##select URL_MEDIO, count(URL_MEDIO) from noticia group by URL_MEDIO; 

##Persona mencionada en una noticia en un dia especifico //Modificar valor de FECHA_PUB
##SELECT NOMBRE, FECHA_PUB FROM persona p 
#JOIN menciona m ON p.ID_PERSONA = m.ID_PERSONA 
#JOIN noticia n ON m.URL_NOTICIA = n.URL_NOTICIA
#WHERE FECHA_PUB = "2022-07-10";


##Evolucion de popularidad de una persona ##
#SELECT ID_PERSONA, VALOR from tiene where ID_PERSONA="1";
cursorObject.execute('SELECT ID_PERSONA, VALOR from tiene where ID_PERSONA="1"')

Lista_POP = list(cursorObject.fetchall())

d1 = [item[1] for item in Lista_POP]
if d1[5] < d1[4]:
  print ("Comparacion Popularidad mes actual con mes anterior: -", round(100 - (d1[0]/d1[1])*100)," %")
elif  d1[5]==d1[4]:
  print ("Comparacion Popularidad mes actual con mes anterior: +0 %")
else:
  print ("Comparacion Popularidad mes actual con mes anterior: +",round (((d1[5]/d1[4])*100)-100)," %")
print(Lista_POP)


##5 medios de prensa mas antiguos de una region 
##SELECT * FROM medio WHERE REGION = "3" ORDER BY FECHA_CRE ASC LIMIT 5;