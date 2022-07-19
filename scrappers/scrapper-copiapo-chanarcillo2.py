import random

def USER_AGENT():
    USER_AGENT_LIST = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
<<<<<<<< HEAD:ScrappersForMerge/AGENT.py
    ]
    rand = random.choice(USER_AGENT_LIST)
    return rand
========
]
headers = {'user-agent':random.choice(USER_AGENT_LIST) }

response = session.get(URL_SEED,headers=headers)

## Analizar ("to parse") el contenido

xpath_url="//article//h2/a/@href"
xpath_date="//time[@class='entry-date published updated']//@datetime"
xpath_date2="//time[@class= 'updated']//@datetime"
xpath_text="//div[@class='entry-content clearfix']//p"

all_urls = response.html.xpath(xpath_url)

def scraper():
    datos_tupla = []
    for url in all_urls:
            article_url = "" + url

            headers = {'user-agent':random.choice(USER_AGENT_LIST) }
            response = session.get(article_url,headers=headers)
            title = response.html.xpath('//div//h1')[0].text

            ##date = find_date(article_url)
            while True: 
                try :
                    date = response.html.xpath(xpath_date)[0]
                    break
                except  (IndexError):
                    date = response.html.xpath(xpath_date2)[0]
                    break

            list_p = response.html.xpath(xpath_text)

            text=""
            for p in list_p:
                    content = p.text
                    content = w3lib.html.remove_tags(content)
                    content = w3lib.html.replace_escape_chars(content)
                    content = html.unescape(content)
                    content = content.strip()
                    text=text+" "+content
            datos_tupla.append(tuple((article_url,title,text,date)))
            
    return datos_tupla

>>>>>>>> origin/main:scrappers/scrapper-copiapo-chanarcillo2.py
