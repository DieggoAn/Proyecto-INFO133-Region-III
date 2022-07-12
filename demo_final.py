import spacy
nlp = spacy.load("es_core_news_md")
print("spacy OK")

import wikipedia
wikipedia.set_lang("es")
import pageviewapi
print("wikipedia OK")

from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from transformers import pipeline
ES_MODEL_LANGUAGE="mrm8488/bert-base-spanish-wwm-cased-finetuned-spa-squad2-es"
tokenizer_es_language = AutoTokenizer.from_pretrained(ES_MODEL_LANGUAGE)
model_es_language = AutoModelForQuestionAnswering.from_pretrained(ES_MODEL_LANGUAGE)
q_a_es = pipeline("question-answering", model=model_es_language, tokenizer=tokenizer_es_language)
print("transformers OK")

import warnings
warnings.filterwarnings("ignore")

#text = """
#El ministro de la Segpres, Giorgio Jackson, se refirió al proyecto que disminuye el quórum para reformar la actual Constitución a 4/7.
#La iniciativa, presentada por los senadores Matías Walker y Ximena Rincón (DC), fue aprobada este martes en la comisión de Constitución de la #Cámara Alta.
#"""


print("--------------------")
def demo_main(documento):
    for ent in documento.ents:
        if ((ent.label_ == "PER") and (" " in ent.text)):
            
            #persona mencionada
            person = ent.text
            print(person)

            #resumen wikipedia
            results= wikipedia.search(person)
            summary= wikipedia.summary(results[1], sentences=3)

            #preguntas
            result = q_a_es(question="¿En qué año nació el o ella?", context=summary)
            print("Nació en "+result["answer"])

            result = q_a_es(question="¿Cuál es su profesión?", context=summary)
            print("Su profesión es "+result["answer"])

            result = q_a_es(question="¿Cuál es su nacionalidad?", context=summary)
            print("Es "+result["answer"])

            try:
                result=pageviewapi.per_article('es.wikipedia', person, '20220705', '20220705',
                                access='all-access', agent='all-agents', granularity='daily')
            except Exception as e:
                print("Error:", e, "al consultar popilaridad en la api")
            else:
                for item in result.items():
                    for article in item[1]:
                        views=article['views']
                        print("Su popularidad hoy es: "+str(views)+" visitas en wikipedia español.")

            print("--------------------")