'''def suma(*arg):
    resultado=0 # Empezamos con un resultado que sea igual a 0
    for i in arg: # Recorremos todos los argumentos
        resultado+=i # Sumamos todos los argumentos
    return resultado

print(suma(1,2,3,4,5))
print(suma(1,2,3,4,5,6,7,8,9,10))'''

'''def suma(**kwargs):
    resultado=0 # Empezamos con un resultado que sea igual a 0
    for i in kwargs: # Recorremos todos los argumentos
        resultado+=kwargs[i] # Sumamos todos los argumentos
    return resultado

print(suma(a=1,b=2,c=3,d=4,e=5))
print(suma(a=1,b=2,c=3,d=4,e=5,f=6,g=7,h=8,i=9,j=10))'''

'''def suma(a: int, b: int, *args, **kwargs) -> int:
    resultado = a + b
    #print(f"El resultado de la suma de a={a} y b={b} es igual a {resultado}")
    for i in args:
        resultado += i
    for clave,valor in kwargs.items():
        print(f"Los valores de **kwargs son: {clave} = {valor}")
    return f"El resultado de *args es: {resultado}"

print(suma(1,2,3,4,5))
print(suma(1,2,3,4,5,6,7,8,9,10))
print(suma(1,2,4,c=2,d=5))

# El resultado de la suma de a=1 y b=2 es igual a 3
# Los valores de **kwargs son: c = 2
# Los valores de **kwargs son: d = 5
# El resultado de *args es: 7'''

agenda = {
    "Ana":    {"telefono": "612345678", "email": "ana@mail.com",    "ciudad": "Madrid"},
    "Luis":   {"telefono": "698765432", "email": "luis@mail.com",   "ciudad": "Barcelona"},
    "Marta":  {"telefono": "611223344", "email": "marta@mail.com",  "ciudad": "Madrid"},
    "Carlos": {"telefono": "655667788", "email": "carlos@mail.com", "ciudad": "Sevilla"},
    "Elena":  {"telefono": "699887766", "email": "elena@mail.com",  "ciudad": "Madrid"},
}
#Extraer todos los nombres
nombres=[nombre for nombre in agenda]
#nombres=agenda.keys()
print(nombres)

#Extraer todos los teléfonos
telefonos=[agenda[nombre]["telefono"] for nombre in agenda]
print(telefonos)

#contactos de Madrid

contactos_madrid=[nombre for nombre in agenda if agenda[nombre]["ciudad"]=="Madrid"]
print(contactos_madrid)

#Extraer todos los emails de los contactos de Madrid
emails_madrid=[agenda[nombre]["email"] for nombre in agenda if agenda[nombre]["ciudad"]=="Madrid"]
print(emails_madrid)

#Crear lista de tuplas (nombre, email)
nombres_emails=[(nombre,agenda[nombre]["email"]) for nombre in agenda]
print(nombres_emails)

#formatear con f-string
fichas = [
    f"📞 {nombre}: {datos['telefono']} ({datos['ciudad']})"
    for nombre, datos in agenda.items()
]
for f in fichas:
    print(f)
# 📞 Ana: 612345678 (Madrid)
# 📞 Luis: 698765432 (Barcelona)
# ...
#Filtrar + transformar (teléfonos que empiezan por "69")
telefonos_69 = [agenda[nombre]["telefono"] for nombre in agenda if agenda[nombre]["telefono"].startswith("69")]
print(telefonos_69)

## Crear un sub-diccionario solo con gente de Madrid
agenda_madrid = {nombre: datos for nombre, datos in agenda.items() if datos["ciudad"] == "Madrid"}
print(agenda_madrid)