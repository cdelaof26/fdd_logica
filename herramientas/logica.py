import herramientas.utilidades as utilidades
from enum import Enum
import re


# Operaciones lógicas y matemáticas


class FuncionLogica(Enum):
    SOP = 0
    POS = 1
    SOP_C = 2
    POS_C = 3
    NA = 4

    def a_cadena(self) -> str:
        if self == self.NA:
            return "ninguno"
        if self == self.SOP:
            return "SOP"
        if self == self.SOP_C:
            return "SOP canónica"
        if self == self.POS:
            return "POS"
        if self == self.POS_C:
            return "POS canónica"

        return ""


def combinar(cantidad_de_entradas: int) -> list:
    combinaciones = list()
    script = ""
    estructura_for = "for v%a in caracteres:"
    caracteres = "01"
    indentado = "    "
    variables = list()

    for i in range(cantidad_de_entradas):
        script += estructura_for % i + "\n" + indentado
        indentado += "    "
        variables.append(f"v{i}")

    script += "combinaciones.append(" + variables[0]
    i = 1
    while i < len(variables):
        script += f" + {variables[i]}"
        i += 1

    exec(script + ")")

    return combinaciones


def capturar_valores_de_salida(combinaciones: list) -> list:
    valores_de_salida = list()

    for combinacion in combinaciones:
        valores_de_salida.append(utilidades.obtener_estado_logico(f"Ingresa el valor de salida para '{combinacion}'"))

    return valores_de_salida


def estructurar_tabla(cantidad_de_variables: int, combinaciones: list, valores_de_salida: list, variables=None):
    tabla = list()
    while len(tabla) < cantidad_de_variables:
        tabla.append(list())

    y = 0
    while y < len(combinaciones):
        for x, valor in enumerate(combinaciones[y]):
            if not tabla[x]:
                if variables is not None:
                    tabla[x].append(variables[x])
                else:
                    tabla[x].append(f"{chr(ord('A') + x)}")
            tabla[x].append(valor)

        y += 1

    tabla.insert(0, ["E"] + list(range(0, y)))

    valores_de_salida.insert(0, "Salida")
    tabla.append(valores_de_salida)

    return tabla


def crear_tabla_de_verdad(variables=None) -> list:
    utilidades.limpiar_pantalla()

    if variables is None:
        cantidad_de_variables = utilidades.obtener_numero_natural("Ingresa la cantidad de variables")
        if cantidad_de_variables == -1:
            return list()
    else:
        cantidad_de_variables = len(variables)

    utilidades.limpiar_pantalla()

    cantidad_de_combinaciones = 2 ** cantidad_de_variables

    if cantidad_de_combinaciones > 16:
        print(f"Se ingresarán {cantidad_de_combinaciones} valores de salida")
        print("¿Continuar?")
        print("1. Si")
        print("2. No")
        if utilidades.seleccionar_opcion(["1", "2"], [False, True]):
            return list()

    combinaciones = combinar(cantidad_de_variables)
    valores_de_salida = capturar_valores_de_salida(combinaciones)

    utilidades.limpiar_pantalla()

    return estructurar_tabla(cantidad_de_variables, combinaciones, valores_de_salida, variables)


def transcribir_a_python(expresion: str):
    while multiplicaciones := re.findall(r"\w{2,}", expresion) + re.findall(r"\w\^\w", expresion):
        for multiplicacion in multiplicaciones:
            nueva_expresion = ""
            agregar_negacion = "^" in multiplicacion

            # Dado que en una misma multiplicación puede existir:
            # x^x, se tiene que procesar dos veces x
            variables_en_multiplicacion = re.findall(r"\w", multiplicacion)

            for variable in variables_en_multiplicacion:
                if variable in multiplicacion:
                    nueva_expresion += variable + "*"

                if agregar_negacion and nueva_expresion and nueva_expresion[-1] == "*" and "^" not in nueva_expresion:
                    nueva_expresion += "^"

            expresion = expresion.replace(multiplicacion, nueva_expresion[:-1])

    multiplicaciones = re.findall(r"\)\^", expresion) + re.findall(r"\)\w", expresion)
    for multiplicacion in multiplicaciones:
        nueva_expresion = ")*" + multiplicacion.replace(")", "")
        expresion = expresion.replace(multiplicacion, nueva_expresion)

    multiplicaciones = re.findall(r"\w\^\(", expresion) + re.findall(r"\w\(", expresion)
    for multiplicacion in multiplicaciones:
        if "^" in multiplicacion:
            nueva_expresion = multiplicacion.replace("^(", "") + "*^("
            expresion = expresion.replace(multiplicacion, nueva_expresion)
        else:
            nueva_expresion = multiplicacion.replace("(", "") + "*("
            expresion = expresion.replace(multiplicacion, nueva_expresion)

    expresion = expresion.replace(")(", ")*(")

    expresion = expresion.replace("^", " not ")
    expresion = expresion.replace("*", " and ")
    expresion = expresion.replace("+", " or ")

    expresion = re.sub(" +", " ", expresion)

    return expresion


def es_expresion_valida(variables: list, expresion: str) -> bool:
    if expresion.count("([{") != expresion.count(")]}"):
        print("  Paréntesis desbalanceado")
        return False

    # No pueden existir dos operadores juntos
    if re.sub(r"[*]{2,}|[+]{2,}", "", expresion) != expresion:
        print("  Operadores juntos")
        return False

    expresion = re.sub(r"[(\[{]", "", expresion)
    expresion = re.sub(r"[]})]", "", expresion)
    expresion = re.sub(r"[\^+*]", "", expresion)
    expresion = expresion.replace(" ", "")

    for variable in variables:
        expresion = expresion.replace(variable, "")

    if expresion:
        print("  Variables en expresión no definidas")
        return False

    return True


def obtener_funcion_booleana(variables=None) -> tuple:
    if variables is None:
        print("Ingresa las variables")
        variables = utilidades.obtener_lista(permitir_elementos_compuestos=False)

    if not variables:
        return [], ""

    utilidades.limpiar_pantalla()

    print("Ingresa la expresión")
    expresion = input("> ").upper()
    expresion = re.sub(r" +", "", expresion)

    if not es_expresion_valida(variables, expresion):
        print("La expresión ingresada no es válida")
        return [], ""

    return variables, expresion


def deducir_tabla_de_verdad(variables=None, expresion=None) -> list:
    utilidades.limpiar_pantalla()

    if variables is None or expresion is None:
        variables, expresion = obtener_funcion_booleana()

    expresion = re.sub(r"[\[{]", "(", expresion)
    expresion = re.sub(r"[]}]", ")", expresion)

    cantidad_de_variables = len(variables)
    combinaciones = combinar(cantidad_de_variables)

    valores_de_salida = list()

    expresion = transcribir_a_python(expresion)
    variables_str = "".join(variables)

    for combinacion in combinaciones:
        expresion_eval = expresion
        for variable, valor in zip(variables_str, combinacion):
            expresion_eval = re.sub(variable + " ", valor + " ", expresion_eval)
            expresion_eval = re.sub(variable + r"\)", valor + ")", expresion_eval)
            expresion_eval = re.sub(variable + "$", valor, expresion_eval)

        expresion_eval = f"valores_de_salida.append({expresion_eval})"
        try:
            exec(expresion_eval)
        except SyntaxError:
            print("  Error al evaluar")
            raise KeyboardInterrupt()

        if valores_de_salida[-1]:
            valores_de_salida[-1] = 1
        else:
            valores_de_salida[-1] = 0

    utilidades.limpiar_pantalla()

    return estructurar_tabla(cantidad_de_variables, combinaciones, valores_de_salida, variables)


def clasificar_expresion(variables: list, expresion: str) -> FuncionLogica:
    if "^(" in expresion:
        # Se considera que nunca se ingresará ^(var)
        # Quizá se corrija después...
        return FuncionLogica.NA

    expresion_sin_negacion = expresion.replace("^", "")

    if "+" not in expresion_sin_negacion:
        return FuncionLogica.NA

    # Procesamiento para POS
    longitud_de_expresion = len(variables) * 2 - 1
    regex_pos_c = r"\([%a+]{%a}\)" % ("".join(variables), longitud_de_expresion)
    cantidad_de_coincidencias = len(re.findall(regex_pos_c, expresion_sin_negacion))

    if re.sub(regex_pos_c, "", expresion_sin_negacion) == "":
        # Dado que se puede ingresar (a+a+a+a), regex podría detectarlo
        # como canónico cuando no lo es
        if utilidades.cadena_contiene_lista_n_veces(expresion_sin_negacion, variables, cantidad_de_coincidencias):
            return FuncionLogica.POS_C

        return FuncionLogica.POS

    if re.sub(r"\([\w+]{3,}\)", "", expresion_sin_negacion) == "" and not re.findall(r"\w{2,}", expresion_sin_negacion):
        return FuncionLogica.POS

    # Procesamiento para SOP
    regex_sop_c = "[%a]{%a}" % ("".join(variables), len(variables))
    regex_sop_c = regex_sop_c + r"\+|" + regex_sop_c
    cantidad_de_coincidencias = len(re.findall(regex_sop_c, expresion_sin_negacion))
    
    if re.sub(regex_sop_c, "", expresion_sin_negacion) == "":
        if utilidades.cadena_contiene_lista_n_veces(expresion_sin_negacion, variables, cantidad_de_coincidencias):
            return FuncionLogica.SOP_C

        return FuncionLogica.SOP

    # Se considerará que funciones como a+bc son SOP
    # temp = re.sub(r"\(\w{2,}\)\+|\(\w{2,}\)", "", expresion_sin_negacion)
    # if re.sub(r"\w{2,}\+|\w{2,}", "", temp) == "":
    #   Puede que se cambie a futuro
    #
    temp = re.sub(r"\(\w+\)\+|\(\w+\)", "", expresion_sin_negacion)
    if re.sub(r"\w+\+|\w+", "", temp) == "":
        return FuncionLogica.SOP

    return FuncionLogica.NA


def extraer_fila_de_tabla(tabla_de_verdad: list, columna_de_salidas: int, y: int) -> list:
    extraccion = list()

    for x in range(1, columna_de_salidas):
        extraccion.append(tabla_de_verdad[x][y])

    return extraccion


def obtener_combinaciones_de_tabla(tabla_de_verdad: list, salida: int) -> list:
    if tabla_de_verdad[-1][0] == "Salida":
        columna_de_salidas = len(tabla_de_verdad) - 1
    else:
        raise ValueError("La tabla no es válida")

    combinaciones = list()

    salida = str(salida)

    y = 0
    while y < len(tabla_de_verdad[columna_de_salidas]):
        if str(tabla_de_verdad[columna_de_salidas][y]) == salida:
            combinaciones.append(extraer_fila_de_tabla(tabla_de_verdad, columna_de_salidas, y))

        y += 1

    return combinaciones


def construir_fc_pos(variables: list, combinaciones0: list) -> str:
    # Si el valor de la variable es 0, se deja tal cual
    # Si el valor de la variable es 1, se complementa

    if not combinaciones0:
        return ""

    fc_pos = ""

    y = 0
    while y < len(combinaciones0):
        fc_pos += "("
        for variable, valor in zip(variables, combinaciones0[y]):
            if valor == "0":
                fc_pos += variable
            else:
                fc_pos += "^" + variable

            fc_pos += "+"

        fc_pos = fc_pos[:-1] + ")"

        y += 1

    return fc_pos


def construir_fc_sop(variables: list, combinaciones1: list) -> str:
    # Si el valor de la variable es 0, se complementa
    # Si el valor de la variable es 1, se deja tal cual

    if not combinaciones1:
        return ""

    fc_sop = ""

    y = 0
    while y < len(combinaciones1):
        for variable, valor in zip(variables, combinaciones1[y]):
            if valor == "0":
                fc_sop += "^" + variable
            else:
                fc_sop += variable

        fc_sop += "+"
        y += 1

    return fc_sop[:-1]


def deducir_expresion(tabla_de_verdad: list) -> list:
    # La tabla debe ser una lista de listas
    if not tabla_de_verdad:
        return ["", ""]
    if not isinstance(tabla_de_verdad[0], list):
        return ["", ""]

    variables = extraer_fila_de_tabla(tabla_de_verdad, len(tabla_de_verdad) - 1, 0)

    funciones = list()

    # POS canónica - maxitérminos (M) [Salida = 0]
    funciones.append(construir_fc_pos(variables, obtener_combinaciones_de_tabla(tabla_de_verdad, 0)))

    # SOP canónica - minitérminos (m) [Salida = 1]
    funciones.append(construir_fc_sop(variables, obtener_combinaciones_de_tabla(tabla_de_verdad, 1)))

    return funciones
