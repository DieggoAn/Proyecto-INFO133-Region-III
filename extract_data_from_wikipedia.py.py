import nltk
import scrapper_atacama_soycopiapo as soycopiapo
import demo_final
import spacy

nlp = spacy.load("es_core_news_md")

dicc_info = soycopiapo.scraping_esp()

def info_wikipedia():
    for i in dicc_info.keys():
        doc = nlp(dicc_info[i]["text"])
        demo_final.demo_main(doc)

info_wikipedia()