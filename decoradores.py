'''def mi_decorador(funcion):
    def nueva_funcion(a, b):
        print("Se va a llamar")
        c = funcion(a, b)
        print("Se ha llamado")
        return c
    return nueva_funcion

@mi_decorador
def suma(a, b):
    print("Entra en funcion suma")
    return a + b    

suma(5,8)

# Se va a llamar
# Entra en funcion suma
# Se ha llamado

@mi_decorador
def resta(a ,b):
    print("Entra en funcion resta")
    return a - b

resta(5, 3)

# Se va a llamar
# Entra en funcion resta
# Se ha llamado

def operaciones(op):
    def suma(a, b):
        return a + b
    def resta(a, b):
        return a - b
    
    if op == "suma":
        return suma
    elif op == "resta":
        return resta
    
funcion_suma = operaciones("suma")
print(funcion_suma(5, 7)) # 12

funcion_suma = operaciones("resta")
print(funcion_suma(5, 7)) # -2'''

#############################################################
'''def decorador(func):
    def envoltorio_func(a, b):
        print("Decorador antes de llamar a la función")
        c = func(a, b)
        print("Decorador después de llamar a la función")
        return c
    return envoltorio_func

def suma(a, b):
    print("Dentro de suma")
    return a + b

# Nueva funcion decorada
funcion_decorada = decorador(suma)

funcion_decorada(5, 8)

def mi_decorador(arg):
    def decorador_real(funcion):
        def nueva_funcion(a, b):
            print(arg)
            c = funcion(a, b)
            print(arg)
            return c
        return nueva_funcion
    return decorador_real

@mi_decorador("Imprimer esto antes y después")
def suma(a, b):
    print("Entra en funcion suma")
    return a + b

suma(5,8)'''
# Imprimer esto antes y después
# Entra en funcion suma
# Imprimer esto antes y después'''
#   

#EJERCICIO CON LOGS.  
def log(fichero_log):
    def decorador_log(func):
        def decorador_funcion(*args, **kwargs):
            with open(fichero_log, 'a') as opened_file:
                output = func(*args, **kwargs)
                opened_file.write(f"{output}\n")
        return decorador_funcion
    return decorador_log

@log('ficherosalida.log')
def suma(a, b):
    return a + b

@log('ficherosalida.log')
def resta(a, b):
    return a - b

@log('ficherosalida.log')
def multiplicadivide(a, b, c):
    return a*b/c

suma(10, 30)
resta(7, 23)
multiplicadivide(5, 10, 2)

'''
#PASO A PASO

#Paso 1: Crear las funciones base sin decorar
#Por qué: Necesitas algo que decorar. Primero defines el comportamiento normal.
def suma(a, b):
    return a + b

def resta(a, b):
    return a - b

def multiplicadivide(a, b, c):
    return a*b/c
Por qué en este orden: Son funciones simples, sin complicaciones. 
Observa que multiplicadivide tiene 3 argumentos mientras que las otras 
tienen 2 → esto será importante más adelante para justificar el uso de *args, **kwargs.

#Paso 2: Llamar a las funciones y verificar
#Por qué: Antes de añadir complejidad, asegúrate de que lo básico funciona.
print(suma(10, 30))        # 40
print(resta(7, 23))        # -16
print(multiplicadivide(5, 10, 2))  # 25.0

#Paso 3: Detectar el problema
#Por qué: Quieres guardar los resultados en un fichero,
#pero no quieres tocar cada función. Aquí nace la idea del decorador.
# ❌ Solución mala: modificar cada función
def suma(a, b):
    resultado = a + b
    with open('ficherosalida.log', 'a') as f:
        f.write(f"{resultado}\n")
    return resultado
# ... y repetir para resta y multiplicadivide
#Por qué es mala: Repites código, mezclas lógica de negocio con lógica de log, 
# y si cambias algo lo tienes que cambiar en 3 sitios.

#Paso 4: Crear el nivel más interno (la función que reemplaza a la original)
#Por qué: Es donde ocurre la acción real. Empiezas por el corazón.

def decorador_funcion(*args, **kwargs):
    output = func(*args, **kwargs)
    # aquí escribiríamos en el fichero

#Por qué *args, **kwargs: Porque tus funciones tienen distinta aridad (2 o 3 argumentos). Necesitas un wrapper que acepte cualquier combinación.
#Por qué aún no abres el fichero: Primero aseguras que la llamada a func funciona.    

#Paso 5: Añadir la apertura del fichero
#Por qué: Ahora que sabes que func se llama correctamente, añades el efecto secundario (escribir en fichero).

def decorador_funcion(*args, **kwargs):
    with open(fichero_log, 'a') as opened_file:
        output = func(*args, **kwargs)
        opened_file.write(f"{output}\n")

#Por qué modo 'a' (append): Para no sobrescribir el fichero en cada llamada.
#Por qué with: Para que el fichero se cierre automáticamente, incluso si hay error.
#Por qué fichero_log no está definido aquí aún: Lo capturará del ámbito enclosing (closure).    
# 
# Paso 6: Envolver con el nivel intermedio (recibe la función)
#Por qué: Necesitas recibir la función a decorar (suma, resta, etc.).   

def decorador_log(func):
    def decorador_funcion(*args, **kwargs):
        with open(fichero_log, 'a') as opened_file:
            output = func(*args, **kwargs)
            opened_file.write(f"{output}\n")
    return decorador_funcion

#Observa: fichero_log aún no está definido en este ámbito. Lo capturará del nivel superior.

#Paso 7: Envolver con el nivel externo (recibe el parámetro)
#Por qué: Quieres que el nombre del fichero sea configurable (@log('ficherosalida.log')).

def log(fichero_log):
    def decorador_log(func):
        def decorador_funcion(*args, **kwargs):
            with open(fichero_log, 'a') as opened_file:
                output = func(*args, **kwargs)
                opened_file.write(f"{output}\n")
        return decorador_funcion
    return decorador_log

#Por qué 3 niveles:
#Nivel 1 (log): recibe el parámetro del decorador ('ficherosalida.log')
#Nivel 2 (decorador_log): recibe la función a decorar
#Nivel 3 (decorador_funcion): recibe los argumentos de la llamada

#Paso 8: Decorar las funciones con @
#Por qué: Es azúcar sintáctico para suma = log('ficherosalida.log')(suma).

@log('ficherosalida.log')
def suma(a, b):
    return a + b

@log('ficherosalida.log')
def resta(a, b):
    return a - b

@log('ficherosalida.log')
def multiplicadivide(a, b, c):
    return a*b/c

#Por qué el mismo fichero para las tres:
#Para que todas las operaciones queden en el mismo log. Podrías usar ficheros distintos si quisieras.

#Paso 10: Leer el fichero para verificar
#Por qué: El decorador no imprime nada en pantalla, solo escribe en fichero. 
# Hay que comprobar el efecto secundario.

'''




#11. Auditoría / Registro de cambios
'''autenticado = False
def requiere_autenticación(f):
    def funcion_decorada(*args, **kwargs):
        if not autenticado:
            print("Error. El usuario no se ha autenticado")
        else:
            return f(*args, **kwargs)
    return funcion_decorada

@requiere_autenticación
def di_hola():
    print("Hola")
    
di_hola()

def auditar(accion):
    """Registra quién hizo qué y cuándo."""
    def decorador(func):
        def wrapper(usuario, *args, **kwargs):
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] {usuario['nombre']} → {accion}: {func.__name__}")
            return func(usuario, *args, **kwargs)
        return wrapper
    return decorador

@auditar("ELIMINAR_USUARIO")
def eliminar_usuario(usuario, id_usuario):
    return f"Usuario {id_usuario} eliminado"

@auditar("CREAR_DOCUMENTO")
def crear_documento(usuario, titulo):
    return f"Documento '{titulo}' creado"

admin = {'nombre': 'Ana', 'rol': 'admin'}
print(eliminar_usuario(admin, 42))
print(crear_documento(admin, "Informe Q4"))

#12. Ejecución solo en horario laboral

from datetime import datetime

def solo_horario_laboral(inicio=9, fin=18):
    """Solo permite ejecutar la función en horario laboral."""
    def decorador(func):
        def wrapper(*args, **kwargs):
            hora = datetime.now().hour
            if inicio <= hora < fin:
                return func(*args, **kwargs)
            else:
                return f" Fuera de horario ({inicio}:00-{fin}:00). Operación aplazada."
        return wrapper
    return decorador

@solo_horario_laboral(inicio=9, fin=18)
def enviar_email(destinatario, asunto):
    return f"📧 Email enviado a {destinatario}: {asunto}"

print(enviar_email("cliente@empresa.com", "Presupuesto"))'''

# Decoradores usados en el ejemplo de combinación.
from datetime import datetime
from functools import wraps

def auditar(accion):
    """Registra quién ejecuta una operación y cuándo."""
    def decorador(func):
        @wraps(func)
        def wrapper(usuario, *args, **kwargs):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] {usuario['nombre']} -> {accion}: {func.__name__}")
            return func(usuario, *args, **kwargs)
        return wrapper
    return decorador

def requiere_rol(roles_permitidos):
    """Permite ejecutar la función solo a usuarios con un rol autorizado."""
    def decorador(func):
        @wraps(func)
        def wrapper(usuario, *args, **kwargs):
            if usuario.get('rol') not in roles_permitidos:
                raise PermissionError("El usuario no tiene permisos suficientes")
            return func(usuario, *args, **kwargs)
        return wrapper
    return decorador

def manejar_excepciones(valor_por_defecto=None):
    """Devuelve un valor por defecto cuando la función produce una excepción."""
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                print(f"Error en {func.__name__}: {error}")
                return valor_por_defecto
        return wrapper
    return decorador

#🎨 Combinación de decoradores
@manejar_excepciones(valor_por_defecto="error")
@requiere_rol(['admin'])
@auditar("ACCESO_SENSIBLE")
def ver_datos_financieros(usuario):
    return {"balance": 15000, "deuda": 3000}

admin = {'nombre': 'Ana', 'rol': 'admin'}
print(ver_datos_financieros(admin))