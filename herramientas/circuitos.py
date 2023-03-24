import herramientas.utilidades as utilidades
import herramientas.logica as logica
import herramientas.recuadro as recuadro
from pathlib import Path
from enum import Enum


COMPUERTAS = ["NOT", "AND", "OR", "NAND", "NOR"]
CIRCUITOS_GUARDADOS = Path("circuitos")


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

    def a_dict(self) -> dict:
        return {
            "NOMBRE": self.nombre,
            "ENTRADAS": self.entradas,
            "CANTIDAD_DE_ENTRADAS": self.cantidad_de_entradas,
            "TABLA_DE_VERDAD": self.tabla_de_verdad,
            "F": self.f,
            "F_SOP": self.f_sop,
            "FC_SOP": self.fc_sop,
            "F_POS": self.f_pos,
            "FC_POS": self.fc_pos
        }

    def a_cadena(self) -> str:
        datos = f"Circuito \"{self.nombre}\"\n"
        datos += "Entradas\t" + str(self.entradas).replace(",", "").replace("'", "") + "\n"
        datos += f"# Entradas\t{self.cantidad_de_entradas}\n"
        datos += f"\n  Tabla de verdad\n{recuadro.crear_tabla(self.tabla_de_verdad)}\n"
        if self.f:
            datos += f"Función\t\t\t{self.f}\n"

        if self.f_sop:
            datos += f"Función SOP\t\t{self.f_sop}\n"

        if self.fc_sop:
            datos += f"Función canónica SOP\t{self.fc_sop}\n"

        if self.f_pos:
            datos += f"Función POS\t\t{self.f_pos}\n"

        if self.fc_pos:
            datos += f"Función canónica POS\t{self.fc_pos}\n"

        return datos


def el_circuito_existe(nombre: str) -> bool:
    global CIRCUITOS_GUARDADOS
    return CIRCUITOS_GUARDADOS.joinpath(nombre + ".json").exists()


def guardar_circuito(circuito: Circuito) -> bool:
    global CIRCUITOS_GUARDADOS

    if not CIRCUITOS_GUARDADOS.exists():
        CIRCUITOS_GUARDADOS.mkdir()

    archivo_nuevo = CIRCUITOS_GUARDADOS.joinpath(circuito.nombre + ".json")

    return utilidades.escribir_archivo(archivo_nuevo, str(circuito.a_dict()))


def crear_circuito(variables=None, funcion_booleana=None, tabla_de_verdad=None) -> Circuito:
    utilidades.limpiar_pantalla()

    print("Ingresa el nombre para el circuito")
    nombre = input("> ")
    if el_circuito_existe(nombre):
        print(f"El circuito \"{nombre}\" ya existe, ¿sobreescribir datos?")
        print("1. Si")
        print("2. No")
        if utilidades.seleccionar_opcion(["1", "2"], [False, True]):
            raise KeyboardInterrupt()

    nuevo_circuito = Circuito(nombre)

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
                nuevo_circuito.tabla_de_verdad = logica.crear_tabla_de_verdad(nuevo_circuito.entradas)

    utilidades.limpiar_pantalla()
    if nuevo_circuito.tabla_de_verdad:
        print("¿Deducir expresiones canónicas de la tabla de verdad?")
        print("1. Si")
        print("2. No")
        if utilidades.seleccionar_opcion(["1", "2"], [True, False]):
            fc_pos, fc_sop = logica.deducir_expresion(nuevo_circuito.tabla_de_verdad)
            nuevo_circuito.set_f(logica.FuncionLogica.POS_C, fc_pos)
            nuevo_circuito.set_f(logica.FuncionLogica.SOP_C, fc_sop)

    guardar_circuito(nuevo_circuito)

    utilidades.limpiar_pantalla()

    return nuevo_circuito
