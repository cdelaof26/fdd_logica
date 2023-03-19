
# Utilidades varias


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
        if opciones is not None:
            print(f"  {len(elementos)} en lista")
            print(lista_de_opciones)
            print("Selecciona una opción")
            seleccion = seleccionar_opcion(opciones, valores)
            if seleccion == "END":
                break
            elementos.append(seleccion)
        else:
            print(f"  {len(elementos)} en lista")
            elemento = input("> ").upper()
            if not elemento:
                break
            elementos.append(elemento)

    return elementos
