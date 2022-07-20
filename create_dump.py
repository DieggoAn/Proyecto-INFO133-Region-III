import os
in_user     = input("Usuario    : ")
os.system(f"mysqldump -u {in_user} -p Atacama > Proyecto_atacama.sql")
print("Dump created successfully")