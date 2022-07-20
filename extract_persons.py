import mysql.connector
#!pip install spacy
#!python -m spacy download es_core_news_md

import spacy
nlp = spacy.load("es_core_news_md")


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

cursorObject.execute('SELECT TEXTO FROM NOTICIA WHERE URL_NOTICIA = "www.mediodeprueba.com/noticias/noticiaFalsa";')

text =str(cursorObject.fetchall())

print (text)

doc = nlp(text)

for ent in doc.ents:
    if ent.label_ == 'PER':
        print(ent.text, ent.label_)
