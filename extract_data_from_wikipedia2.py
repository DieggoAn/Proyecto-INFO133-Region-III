#pip install git+https://github.com/Commonists/pageview-api.git
#pip install transformers
# o pip install transformers[torch]
import pageviewapi

from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from transformers import pipeline

import wikipedia
wikipedia.set_lang("es")
##p = wikipedia.page("Gabriel Boric")
content = (wikipedia.summary("Gabriel Boric", sentences=3))


ES_MODEL_LANGUAGE="mrm8488/bert-base-spanish-wwm-cased-finetuned-spa-squad2-es"

tokenizer_es_language = AutoTokenizer.from_pretrained(ES_MODEL_LANGUAGE)
model_es_language = AutoModelForQuestionAnswering.from_pretrained(ES_MODEL_LANGUAGE)

q_a_es = pipeline("question-answering", model=model_es_language, tokenizer=tokenizer_es_language)

result3= q_a_es(question="¿Cual es su nombre?", context=content)
result = q_a_es(question="¿En qué año nació el o ella?", context=content)
result2 = q_a_es(question="¿Cual es la profesión de el o ella?",context=content)
print("Nombre: ",result3["answer"])
print("Nació en: ",result["answer"])
print("Ocupacion",result2["answer"])


result1=pageviewapi.per_article('es.wikipedia', 'Gabriel Boric', '20220101', '20220701',
                        access='all-access', agent='all-agents', granularity='monthly')

visitas = []
for item in result1.items():
    for article in item[1]:
        timestamp=article['timestamp'][:8] #first 8 digits
        views=article['views']
        visitas.append(views) 

print ("Visitas este mes: ", visitas[-1])
if visitas[-1] < visitas[-2]:
  print ("Comparacion Popularidad mes actual con mes anterior: -", round(100 - (visitas[-1]/visitas[-2])*100)," %")
elif  visitas[-1]==visitas[-2]:
  print ("Comparacion Popularidad mes actual con mes anterior: +0 %")
else:
  print ("Comparacion Popularidad mes actual con mes anterior: +",round (((visitas[-1]/visitas[-2])*100)-100)," %")
