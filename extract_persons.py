import spacy
import scrapper_atacama_soycopiapo as soycopiapo
nlp = spacy.load("es_core_news_md")

dicc_info = soycopiapo.scraping_data()

def menciones_soycopiapo():
    list_men = []
    for i in dicc_info.keys():
        text = dicc_info[i]["text"]
        doc = nlp(text)
        for ent in doc.ents:
            if ((ent.label_ == "PER") and (" " in ent.text)):
                list_men.append(ent.text)
    return list_men

#Esta es la funcion que ejecuta lo pedido
#print(menciones_soycopiapo())