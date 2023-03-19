import herramientas.utilidades as utilidades
from enum import Enum


COMPUERTAS = ["NOT", "AND", "OR", "NAND", "NOR"]


class Compuerta(Enum):
    NOT = 0
    AND = 1
    OR = 2
    NAND = 3
    NOR = 4


class Circuito:
    def __init__(self, nombre):
        self.nombre = nombre
        self.entradas = list()
        self.cantidad_de_entradas: int
        self.tabla_de_verdad: dict
        self.f_sop: str
        self.fc_sop: str
        self.f_pos: str
        self.fc_pos: str


def crear_circuito() -> Circuito:
    nuevo_circuito = Circuito("unnamed")

    print("Ingresa las entradas")
    nuevo_circuito.entradas = utilidades.obtener_lista()
    nuevo_circuito.cantidad_de_entradas = len(nuevo_circuito.entradas)

    return nuevo_circuito


"""
def trascribir_compuerta(variable: str, compuerta: str) -> str:
    if Compuerta[compuerta] == Compuerta.NOT:
        return "^" + variable

    if Compuerta[compuerta] == Compuerta.AND:
        return variable + "*"

    if Compuerta[compuerta] == Compuerta.OR:
        return variable + "+"

    return variable


def ensamblar_expresiones(expresiones: list) -> list:
    expresiones_ensambladas = list()

    for expresion in expresiones:
        variable = expresion[0]
        i = 1
        expresiones_ensambladas.append(variable)
        expresiones_trasncritas = list()
        while i < len(expresion):
            transcripcion = trascribir_compuerta(variable, expresion[i])
            if transcripcion not in expresiones_ensambladas or "^" not in transcripcion:
                expresiones_ensambladas.append(transcripcion)
                # expresiones_trasncritas.append(transcripcion)
            i += 1

        # expresiones_ensambladas.append(expresiones_trasncritas)

    return expresiones_ensambladas


def unir_expresiones(expresion1: str, expresion2: str) -> str:
    global COMPUERTAS

    if expresion2[-1] == "*" and expresion1[-1] == "*" or expresion2[-1] == "+" and expresion1[-1] == "+":
        print("¿Como deberían unirse las expresiones?")
        union1 = unir_expresiones(expresion1, expresion2[:-1])
        union2 = expresion1 + expresion2
        print("1.", union1)
        print("2.", union2)
        return utilidades.seleccionar_opcion(["1", "2"], [union1, union2])

    if expresion1[-1] == "*" or expresion1[-1] == "+":
        return expresion1 + expresion2

    if not expresion2[-1] == "*" and not expresion2[-1] == "+":
        print(f"¿Qué operador une las expresiones \"{expresion1}\" y \"{expresion2}\"?")
        lista_de_compuertas, opciones = utilidades.enumerar_lista(COMPUERTAS)
        print(lista_de_compuertas)
        operador = utilidades.seleccionar_opcion(opciones, COMPUERTAS)
        unir_expresiones(trascribir_compuerta(expresion1, operador), expresion2)
        # raise ValueError(f"Las expresiones \"{expresion1}\" y \"{expresion2}\" no tienen un operador")

    return f"{expresion1}{expresion2[-1]}{expresion2[:-1]}"


def mapear_circuito():
    global COMPUERTAS

    ###print("Ingresa las variables")
    variables = utilidades.obtener_lista()

    expresiones = list()

    for variable in variables:
        print(f"Ingresa la lista de compuertas con las que se relaciona {variable}")
        lista = [variable] + utilidades.obtener_lista(COMPUERTAS)
        expresiones.append(lista) ###

    # print("res", expresiones)
    # expresiones = [["A", "NOT", "AND", "OR"], ["B", "AND", "OR"]]
    expresiones = [['A', 'AND'], ['B', 'AND', 'NOT', 'AND'], ['C', 'NOT']]

    expresiones = ensamblar_expresiones(expresiones)

    circuito = ""

    expresiones += ["" + "Terminar"]
    lista_de_opciones, opciones = utilidades.enumerar_lista(expresiones)

    while True:
        print(f"Función booleana: {circuito}")

        print(f"Selecciona un termino")
        print(lista_de_opciones)
        seleccion = utilidades.seleccionar_opcion(opciones, expresiones)

        if seleccion == "Terminar":
            break

        if not circuito:
            circuito = seleccion
            continue

        circuito = unir_expresiones(circuito, seleccion)

    print(circuito)

    ###i = 0
    while len(expresiones) > 1:
        expresion = expresiones[i]
        expresiones.pop(i)

        expresiones += ["Ninguno"]
        lista_de_opciones, opciones = utilidades.enumerar_lista(expresiones)

        print(f"Selecciona el termino con el que se relaciona {expresion}")
        print(lista_de_opciones)

        seleccion = utilidades.seleccionar_opcion(opciones, expresiones)
        expresiones = expresiones[:-1]
        if seleccion == "Ninguno":
            expresiones.insert(i, expresion)
            i += 1
            if i == len(expresiones):
                i = 0
            continue

        expresiones.insert(i, unir_expresiones(expresion, seleccion))
        expresiones.remove(seleccion)###
"""
