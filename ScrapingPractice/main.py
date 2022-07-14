import chanarcilloNews

newslist = chanarcilloNews.searchItem()
dataa = chanarcilloNews.formatDB(newslist)
for i in dataa:
    print(i,"")
#chanarcilloNews.printNews(newslist,1)

"""
print("Los medios estan etiquetados por numeros: \n  1 -> soychile")
print("  2 -> Chanarcillo \n  3 -> Atacama \n  4 -> MMMMMMMM \n  5 ->XXXXXXXX \n ")
x=-1
while not(x>0 and x<=5):
    x = int(input("Ingrese Medio del que desea obtener las noticias: "))
"""