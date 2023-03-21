import herramientas.utilidades as utilidades
import re


# Operaciones lógicas y matemáticas


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
        salida_valida = False
        valor_de_salida = ""
        while not salida_valida:
            print(f"Ingresa el valor de salida para '{combinacion}'")
            valor_de_salida = input("> ")
            salida_valida = valor_de_salida == "0" or valor_de_salida == "1"
            if not salida_valida:
                print("Valor invalido")

        valores_de_salida.append(valor_de_salida)

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
                    tabla[x].append(f"V{x}")
            tabla[x].append(valor)

        y += 1

    tabla.insert(0, ["E"] + list(range(0, y)))

    valores_de_salida.insert(0, "Salida")
    tabla.append(valores_de_salida)

    return tabla


def crear_tabla_de_verdad() -> list:
    utilidades.limpiar_pantalla()

    print("Ingresa la cantidad de variables")
    cantidad_de_variables = input("> ")

    if re.sub(r"\d", "", cantidad_de_variables):  # La cadena no es vacía
        print("   Los datos ingresados no son válidos")
        return list()

    cantidad_de_variables = int(cantidad_de_variables)
    if cantidad_de_variables == 0:
        print("   No es posible crear una tabla con 0 variables")
        return list()

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

    return estructurar_tabla(cantidad_de_variables, combinaciones, valores_de_salida)


def transcribir_a_python(variables: list, expresion: str):
    while multiplicaciones := re.findall(r"\w{2,}", expresion) + re.findall(r"\w\^\w", expresion):
        for multiplicacion in multiplicaciones:
            nueva_expresion = ""
            agregar_negacion = "^" in multiplicacion

            for variable in variables:
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
            print("bf", nueva_expresion)
            expresion = expresion.replace(multiplicacion, nueva_expresion)
        else:
            nueva_expresion = multiplicacion.replace("(", "") + "*("
            print("bf", nueva_expresion)
            expresion = expresion.replace(multiplicacion, nueva_expresion)

        print("af", expresion)

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
    if re.findall(f"\*{2,}|\+{2,}", expresion):
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


def deducir_tabla_de_verdad() -> list:
    utilidades.limpiar_pantalla()

    print("Ingresa las variables")
    variables = utilidades.obtener_lista()

    if not variables:
        return list()

    print("Ingresa la expresión")
    expresion = input("> ").upper()

    if not es_expresion_valida(variables, expresion):
        print("La expresión ingresada no es válida")
        return list()

    expresion = re.sub(r"[\[{]", "(", expresion)
    expresion = re.sub(r"[]}]", ")", expresion)

    cantidad_de_variables = len(variables)
    combinaciones = combinar(cantidad_de_variables)

    valores_de_salida = list()

    expresion = transcribir_a_python(variables, expresion)
    variables_str = "".join(variables)

    for combinacion in combinaciones:
        expresion_eval = expresion
        for variable, valor in zip(variables_str, combinacion):
            expresion_eval = re.sub(variable + " ", valor + " ", expresion_eval)
            expresion_eval = re.sub(variable + r"\)", valor + ")", expresion_eval)
            expresion_eval = re.sub(variable + "$", valor, expresion_eval)

        expresion_eval = f"valores_de_salida.append({expresion_eval})"
        exec(expresion_eval)
        if valores_de_salida[-1]:
            valores_de_salida[-1] = 1
        else:
            valores_de_salida[-1] = 0
        # valores_de_salida.append(salida)

    return estructurar_tabla(cantidad_de_variables, combinaciones, valores_de_salida, variables)
