from cgitb import text
from colorama import Cursor
import mysql.connector
import msvcrt
 
 #INPUT MODE
 # -> 1 (TUPLA SQL "(DATO1,DATO2,DATO3,...,DATON)")
INPUT_MODE = 1
INPUT_DATO=3
VIEW_MODE = 2
VIEW_DATO =4

TABLAS = {
  "N/A" : ["N","A"],
  #Tablas Simples
  "dueno" : ["ID_DUENO","NOMBRE","TIPO"],
  "medio" : ["URL_MEDIO","NOMBRE","PAIS","IDIOMA","REGION","FECHA_CRE"],
  "persona" : ["ID_PERSONA","WIKI","NOMBRE","PROFESION","NACIONALIDAD","FECHA_NAC"],
  "popularidad" : ["FECHA_POP"],
  #Tablas Dependientes
  "noticia" : ["URL_NOTICIA","TITULO","TEXTO","FECHA_PUB","URL_MEDIO"],
  #Tablas Intermedias
  "adquiere" : ["ID_DUENO","URL_MEDIO","FECHA_ADQ"],
  "menciona" : ["ID_PERSONA","URL_NOTICIA"],
  "tiene" : ["ID_PERSONA","FECHA_POP","VALOR"]
}

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


def SelecTablaASCII():
    textASCII = "Seleciona una tabla:"
    cursorObject.execute("SHOW TABLES;")
    num_opc = 1
    for i in cursorObject:
      textASCII = textASCII + "\n{}) ".format(num_opc) + i[0]
      num_opc += 1
    textASCII += "\n>>>"
    return textASCII

def textASCII(mode=INPUT_MODE,tabla="N/A"):
    if mode == INPUT_MODE:
      textASCII = "[=][INGRESO DE DATOS[=]\n"
      textASCII += SelecTablaASCII()
    elif mode == INPUT_DATO:
      textASCII = "[=][TABLA SELECCIONADA: {}][=]\nForma de ingreso de datos: {}".format(tabla,TABLAS[tabla]).replace("[","(").replace("]",")") + "\n>>>"
    elif mode == VIEW_MODE:
      textASCII = "[=][VER DATOS[=]\n"
      textASCII += SelecTablaASCII()
    elif mode == VIEW_DATO:
      textASCII = "[=][ TABLA SELECCIONADA: {} ][=]".format(tabla).replace("[","(").replace("]",")") + "\n>>>"
    return textASCII

def anadirDatoASCII(tabla):
  bucle_dato = True
  while bucle_dato:
    dato = input(textASCII(INPUT_DATO,tabla))
    if dato == "0":
      bucle_dato = False
    else:
      try:
        cursorObject.execute("INSERT INTO {} {} ".format(tabla,TABLAS[tabla]).replace("[","(").replace("]",")").replace("'","") + " VALUES {};".format(dato))
      except Exception as e:
        print("Error:", type(e).__name__ )
      else:
        dataBase.commit()
        print("Añadido " + dato + " a la tabla " + tabla)
        bucle_dato = False

def verDatoASCII(tabla):
  cursorObject.execute("SELECT * FROM {};".format(tabla))
  print("{}".format(TABLAS[tabla]).replace("[","(").replace("]",")").replace("'",""))
  for i in cursorObject:
    print(i)
  print("Presione una tecla para continuar...")
  msvcrt.getch()
  

def tablaSelecionada(numero):
  cursorObject.execute("SHOW TABLES;")
  num_opc = 1
  tabla = "N/A"
  for i in cursorObject:
    if num_opc == numero:
      tabla = i[0]        
      return tabla
    num_opc += 1
  return tabla

def AppASCII(mode=INPUT_MODE):
  if mode == INPUT_MODE or mode == VIEW_MODE:
    ##SET ASCII MODE
    bucle_opc = True
    while bucle_opc:
      try:
        comando = int(input(textASCII(mode,"N/A")))
      except Exception as e:
        print("Error:", type(e).__name__)
      else:
        if comando == 0:
          bucle_opc = False
        #Comando entre 1 y el N° de tablas
        elif comando >= 1 and comando <= 8:
          tabla = tablaSelecionada(comando)
          if mode == INPUT_MODE:
            anadirDatoASCII(tabla)
          elif mode == VIEW_MODE:
            verDatoASCII(tabla)
        #Cambio de modo a view
        elif comando == -1:
          if mode == INPUT_MODE:
            mode = VIEW_MODE
          elif mode == VIEW_MODE:
            mode = INPUT_MODE
        else:
          print("Opcion no existe.")
  else:
    print("Error de modo. Restableciendo a INPUT_MODE.")
    AppASCII(INPUT_MODE)



AppASCII()

#baseDueno = "INSERT IGNORE INTO  DUENO (ID_DUENO_PK, NOMBRE, TIPO) VALUES (1, 'Julio', 'Persona')"
#baseMedio = "INSERT IGNORE INTO MEDIO (URL_MEDIO_PK, NOMBRE, PAIS, IDIOMA, REGION, FECHA_CRE) VALUES('www.pagina.com', 'nombre', 'Chile', 'Espanol',3, '1999-09-24')"
#basePersona = "INSERT IGNORE INTO PERSONA(ID_PERSONA_PK, POPULARIDAD, WIKI, NOMBRE, PROFESION, NACIONALIDAD, FECHA_NAC) VALUES(01, 100, 'www.wikipedia.com', 'Felipe', 'Profesor', 'Chilena','1999-02-27')"
#baseNoticia = "INSERT IGNORE INTO NOTICIA(URL_NOTICIA_PK, TITULO, TEXTO, FECHA_PUB, URL_MEDIO_FK) VALUES('www.otrapagina.com', 'Hola' , 'chao.','2022-06-22', 'www.pagina.com')"
#baseAdquiere = "INSERT IGNORE INTO ADQUIERE(ID_DUENO_FK, URL_MEDIO_FK, FECHA_ADQ) VALUES (1,'www.pagina.com', '1930-07-19')"
#baseMenciona = "INSERT IGNORE INTO MENCIONA(ID_PERSONA_FK, URL_NOTICIA_FK) VALUES (01,'www.otrapagina.com')"
#basePopularidad = "INSERT IGNORE INTO POPULARIDAD(ID_PERSONA_FK, FECHA, VALOR) VALUES (01, '2022-06-22', 100)"


#cursorObject.execute(baseDueno)
#cursorObject.execute(baseMedio)
#cursorObject.execute(basePersona)
#cursorObject.execute(baseNoticia)
#cursorObject.execute(baseAdquiere)
#cursorObject.execute(baseMenciona)
#cursorObject.execute(basePopularidad)

#dataBase.commit()
                 
       