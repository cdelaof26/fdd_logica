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
