import herramientas.utilidades as utilidades
import herramientas.logica as logica
import herramientas.recuadro as recuadro
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
        self.cantidad_de_entradas = 0
        self.tabla_de_verdad = list()
        self.f_definida = False
        self.f = ""
        self.f_sop = ""
        self.fc_sop = ""
        self.f_pos = ""
        self.fc_pos = ""

    def get_f(self) -> str:
        if not self.f_definida:
            return ""

        if self.f:
            return self.f
        if self.f_sop:
            return self.f_sop
        if self.fc_sop:
            return self.fc_sop
        if self.f_pos:
            return self.f_pos
        if self.fc_pos:
            return self.fc_pos

    def set_f(self, tipo: logica.FuncionLogica, expresion: str):
        if tipo == logica.FuncionLogica.NA:
            self.f = expresion
        elif tipo == logica.FuncionLogica.SOP:
            self.f_sop = expresion
        elif tipo == logica.FuncionLogica.SOP_C:
            self.fc_sop = expresion
        elif tipo == logica.FuncionLogica.POS:
            self.f_pos = expresion
        elif tipo == logica.FuncionLogica.POS_C:
            self.fc_pos = expresion

    def a_cadena(self) -> str:
        datos = f"Circuito \"{self.nombre}\"\n"
        datos += "Entradas\t" + str(self.entradas).replace(",", "").replace("'", "") + "\n"
        datos += f"# Entradas\t{self.cantidad_de_entradas}\n"
        datos += f"\n  Tabla de verdad\n{recuadro.crear_tabla(self.tabla_de_verdad)}\n"
        datos += f"Función\t\t\t{self.f}\n"
        datos += f"Función SOP\t\t{self.f_sop}\n"
        datos += f"Función canónica SOP\t{self.fc_sop}\n"
        datos += f"Función POS\t\t{self.f_pos}\n"
        datos += f"Función canónica POS\t{self.fc_pos}\n"

        return datos


def crear_circuito(variables=None, funcion_booleana=None, tabla_de_verdad=None) -> Circuito:
    utilidades.limpiar_pantalla()

    print("Ingresa el nombre para el circuito")
    nuevo_circuito = Circuito(input("> "))

    if variables is None:
        utilidades.limpiar_pantalla()

        print("Ingresa las entradas")
        nuevo_circuito.entradas = utilidades.obtener_lista()
    else:
        nuevo_circuito.entradas = variables

    nuevo_circuito.cantidad_de_entradas = len(nuevo_circuito.entradas)

    utilidades.limpiar_pantalla()
    if funcion_booleana is None:
        print("¿Agregar la expresión de la función?")
        print("1. Si")
        print("2. No")
        if utilidades.seleccionar_opcion(["1", "2"], [True, False]):
            _, expresion = logica.obtener_funcion_booleana(nuevo_circuito.entradas)
            if expresion:
                nuevo_circuito.f_definida = True
                tipo = logica.clasificar_expresion(nuevo_circuito.entradas, expresion)
                nuevo_circuito.set_f(tipo, expresion)

    utilidades.limpiar_pantalla()
    if tabla_de_verdad is None:
        print("¿Agregar la tabla de verdad?")
        print("1. Si")
        print("2. No")
        if utilidades.seleccionar_opcion(["1", "2"], [True, False]):
            if nuevo_circuito.f_definida:
                nuevo_circuito.tabla_de_verdad = \
                    logica.deducir_tabla_de_verdad(nuevo_circuito.entradas, nuevo_circuito.get_f())
            else:
                nuevo_circuito.tabla_de_verdad = logica.crear_tabla_de_verdad(variables)

    utilidades.limpiar_pantalla()
    if nuevo_circuito.tabla_de_verdad and not nuevo_circuito.f_definida:
        print("¿Deducir expresiones de la tabla de verdad?")
        print("1. Si")
        print("2. No")
        if utilidades.seleccionar_opcion(["1", "2"], [True, False]):
            pass

    return nuevo_circuito
