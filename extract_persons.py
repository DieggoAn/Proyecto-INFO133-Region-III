import spacy
import scrappers.atacama_soycopiapo as soycopiapo
nlp = spacy.load("es_core_news_md")

textos = soycopiapo.scrap_text()

def menciones_soycopiapo():
    list_men = []
    for texto in textos:
        doc = nlp(texto)
        for ent in doc.ents:
            if ((ent.label_ == "PER") and (" " in ent.text)):
                list_men.append(ent.text)
    return list_men
    

print(menciones_soycopiapo())