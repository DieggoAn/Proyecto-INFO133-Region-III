import extract_persons

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

list_menciones = extract_persons.menciones_soycopiapo()

for persona in list_menciones:
      results= wikipedia.search(persona)
      summary= wikipedia.summary(results[1], sentences=3)

      #preguntas
      result = q_a_es(question="¿En qué año nació el o ella?", context=summary)
      print("Nació en "+result["answer"])

      result = q_a_es(question="¿Cuál es su profesión?", context=summary)
      print("Su profesión es "+result["answer"])

      result = q_a_es(question="¿Cuál es su nacionalidad?", context=summary)
      print("Es "+result["answer"])

      try:
            result=pageviewapi.per_article('es.wikipedia', persona, '20220705', '20220705',
                              access='all-access', agent='all-agents', granularity='daily')
      except Exception as e:
            print("Error:", e, "al consultar popilaridad en la api")
      else:
            for item in result.items():
                  for article in item[1]:
                        views=article['views']
                        print("Su popularidad hoy es: "+str(views)+" visitas en wikipedia español.")