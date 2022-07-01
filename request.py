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

def noticiasPublicadas():
      cursorObject.execute("SELECT URL_NOTICIA,URL_MEDIO FROM NOTICIA;")
      for i in cursorObject:
            print(i)

noticiasPublicadas()
