from subprocess import call
import re

# Utilidades varias


NOMBRE_DEL_SISTEMA = ""


def obtener_nombre_del_sistema():
    global NOMBRE_DEL_SISTEMA

    try:
        from os import uname
        NOMBRE_DEL_SISTEMA = uname()[0]
    except ImportError:
        NOMBRE_DEL_SISTEMA = "nt"


def limpiar_pantalla():
    global NOMBRE_DEL_SISTEMA

    if not NOMBRE_DEL_SISTEMA:
        obtener_nombre_del_sistema()

    if NOMBRE_DEL_SISTEMA == "nt":
        call("cls", shell=True)
    else:
        call("clear", shell=True)


def seleccionar_opcion(opciones: list, valores=None):
    seleccion = ""

    while not seleccion:
        seleccion = input("> ").upper()
        if seleccion not in opciones:
            print("Opción invalida!")
            seleccion = ""

    if valores is not None:
        return valores[opciones.index(seleccion)]

    return seleccion


def obtener_numero_natural(instruccion: str) -> int:
    print(instruccion)
    numero = input("> ")

    if re.sub(r"\d", "", numero):  # La cadena no es vacía
        print("   Los datos ingresados no son válidos")
        return -1

    numero = int(numero)
    if numero < 1:  # Excluimos el cero
        print("   El dato no esta en el rango permitido: [0, inf]")
        return -1

    return numero


def enumerar_lista(lista: list) -> tuple:
    lista_imprimible = ""
    opciones = list()

    for i, opcion in enumerate(lista):
        i += 1
        lista_imprimible += f"{i}. {opcion}\n"
        opciones.append(f"{i}")

    return lista_imprimible[:-1], opciones


def obtener_lista(opciones=None) -> list:
    elementos = list()
    lista_de_opciones = ""
    valores = list()

    if opciones is not None:
        valores = opciones.copy() + ["END"]
        lista_de_opciones, opciones = enumerar_lista(opciones + ["Terminar"])

    while True:
        print("Ingresa una cadena vacía para terminar")
        if opciones is not None:
            print("  Elementos ingresados: {0}".format(str(elementos).replace(",", "").replace("'", '')))
            print(lista_de_opciones)
            print("Selecciona una opción")
            seleccion = seleccionar_opcion(opciones, valores)
            if seleccion == "END":
                break
            elementos.append(seleccion)
        else:
            print("  Elementos ingresados: {0}".format(str(elementos).replace(",", "").replace("'", '')))
            elemento = input("> ").upper()
            if not elemento:
                break
            elementos.append(elemento)

        limpiar_pantalla()

    return elementos


def cadena_contiene_lista_n_veces(cadena: str, lista: list, veces: int) -> bool:
    for elemento in lista:
        if cadena.count(elemento) != veces:
            print("count", cadena.count(elemento), "expected", veces, "for", elemento)
            return False

    return True
