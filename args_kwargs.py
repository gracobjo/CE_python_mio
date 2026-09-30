def funcion(a, b, *args, **kwargs):
    print("a =", a)
    print("b =", b)
    for arg in args:
        print("args =", arg)
    for key, value in kwargs.items():
        print(key, "=", value)

funcion(10, 20, 1, 2, 3, 4, x="Hola", y="Que", z="Tal")
#Salida
#a = 10
#b = 20
#args = 1
#args = 2
#args = 3
#args = 4
#x = Hola
#y = Que
#z = Tal

#TUPLE UNPACKING
def funcion(a, b, *args, **kwargs):
    print("a =", a)
    print("b =", b)
    for arg in args:
        print("args =", arg)
    for key, value in kwargs.items():
        print(key, "=", value)

args = [1, 2, 3, 4]
kwargs = {'x':"Hola", 'y':"Que", 'z':"Tal"}

funcion(10, 20, *args, **kwargs)
#Salida
#a = 10
#b = 20
#args = 1
#args = 2
#args = 3
#args = 4
#x = Hola
#y = Que
#z = Tal