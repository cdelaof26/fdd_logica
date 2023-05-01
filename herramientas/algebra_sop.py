from herramientas import algebra
from herramientas import logica
from herramientas import utilidades
import re

# Utilidades para la reducción de funciones tipo SOP


def generar_terminos_reducibles(variables: list) -> list:
	# Los términos generados deben usarse con regex

	terminos = list()
	for variable in variables:
		terminos.append([f"[(]{variable}" + r"[+][\^]" + f"{variable}[)]", ""])
		terminos.append([r"[(][\^]" + f"{variable}[+]{variable}[)]", ""])
		# terminos.append([f"{variable}" + r"[+][\^]" + variable + r"(?=[+)])", "1"])
		terminos.append([f"[+]{variable}" + r"[+][\^]" + variable + r"(?=[+)])", "+1"])
		terminos.append([f"[(]{variable}" + r"[+][\^]" + variable + r"(?=[+)])", "(1"])

		terminos.append([r"[\^]" + f"{variable}[+]{variable}" + r"(?=[+)])", "1"])
		terminos.append([r"[(]" + f"{variable}[)]", variable])
		terminos.append([r"[(][\^]" + f"{variable}[)]", f"^{variable}"])

	return terminos


def reducir_terminos(terminos_reducibles: list, expresion: str) -> str:
	expresion += " "

	for termino in terminos_reducibles:
		expresion = re.sub(termino[0], termino[1], expresion)

	expresion = re.sub("[(][)]", "", expresion)

	return expresion.strip()


def termino_a_regex(termino: str) -> str:
	return termino.replace("^", r"[\^]").replace("+", r"[+]").replace("(", "[(]").replace(")", "[)]")


def reducir_a_or_ab(expresion: str) -> str:
	if not expresion:
		return ""

	# A + AB = A
	# ^A + ^AB = ^A
	miniterminos = expresion.split("+")

	j = 0
	while j < len(miniterminos):
		busqueda = "^" + miniterminos[j].replace("^", r"[\^]")

		i = 0
		while i < len(miniterminos):
			if i != j and re.findall(busqueda, miniterminos[i]):
				miniterminos.pop(i)
				j = -1
				break

			i += 1

		j += 1

	return "+".join(miniterminos)


def reducir_a_or_not_a_and_b(expresion: str) -> str:
	if not expresion:
		return ""

	# A + ^AB = A+B  - Caso 1
	# ^A + AB = ^A+B - Caso 2
	miniterminos = expresion.split("+")

	j = 0
	while j < len(miniterminos):
		es_caso_1 = miniterminos[j][0] != '^'

		if es_caso_1:
			if len(miniterminos[j]) > 1:
				# No se considera por ahora el caso donde el minitérmino tiene más de una variable
				# 	Como AB, ABC, ABCD, etc.
				# busqueda = r"[\^][(]" + miniterminos[j].replace("^", r"[\^]") + r"[)]\w+"
				j += 1
				continue
			else:
				busqueda = r"[\^]" + miniterminos[j] + r"[\w\^]+"
		else:
			busqueda = "^" + re.sub(".", "", miniterminos[j], 1) + r"[\w\^]+"

		i = 0
		while i < len(miniterminos):
			if i != j and re.findall(busqueda, miniterminos[i]):
				miniterminos[i] = re.sub(busqueda.replace("[\\w\\^]+", ""), "", miniterminos[i])

			i += 1

		j += 1

	return "+".join(miniterminos)


def remover_termino(variable: str, termino: str) -> str:
	return termino.replace(f"^{variable}", "").replace(variable, "")


def factorizar_expresion(variables: list, expresion: str) -> str:
	if not expresion:
		return ""

	miniterminos = expresion.split("+")[::-1]
	if len(miniterminos) == 1:
		return expresion

	variable_a_remover = len(variables) - 1

	busqueda_inicial = ""
	busqueda = ""
	resultados = list()
	factorizaciones = list()

	orden_reverso = False
	expresion_de_entrada = expresion

	j = 0
	while j < len(miniterminos):
		if variable_a_remover == len(variables) - 1:
			resultados = list()
			busqueda = miniterminos[j]
			busqueda_inicial = busqueda

		i = 0
		while i < len(miniterminos):
			if i != j and busqueda in miniterminos[i]:
				if f"^{busqueda}" not in miniterminos[i] and busqueda in miniterminos[i]:
					resultados.append(miniterminos[i])

			i += 1

		if resultados:  # Se encontraron términos semejantes factorizables
			for i, termino in enumerate(resultados):
				miniterminos.remove(termino)
				resultados[i] = termino.replace(busqueda, "")

			miniterminos.remove(busqueda_inicial)
			factorizacion = f"{busqueda}({busqueda_inicial.replace(busqueda, '')}+{'+'.join(resultados)})"

			factorizaciones.append(factorizacion)

			if miniterminos:
				expresion = "+".join(miniterminos) + "+" + "+".join(factorizaciones)
			else:
				expresion = "+".join(factorizaciones)

			variable_a_remover = len(variables) - 1
			j = 0
			continue

		busqueda = remover_termino(variables[variable_a_remover], busqueda)
		variable_a_remover -= 1

		if variable_a_remover == -1 or busqueda == "":
			variable_a_remover = len(variables) - 1
			j += 1

		if j == len(miniterminos):
			if expresion == expresion_de_entrada and not orden_reverso:
				orden_reverso = True
				variables = variables[::-1]
				j = 0

	return expresion


def factorizar_expresion_factorizada(expresion: str) -> str:
	# Factoriza una expresión del tipo
	#     A(BC+CD)+^A(BC+CD) -> (A+^A)(BC+CD)
	if "(" not in expresion:
		return expresion

	miniterminos = re.findall(r"[\w^]+[(][\w^+]+[)]", expresion)

	expresion_prueba = expresion
	for minitermino in miniterminos:
		minitermino = termino_a_regex(minitermino)
		expresion_prueba = re.sub(minitermino, "", expresion_prueba)

	if re.sub("[+]", "", expresion_prueba):  # No todos los elementos son factorizables
		return expresion

	elementos_factorizados = list()

	for termino in miniterminos:
		elementos_factorizados.append(re.findall(r"[(][\w^+]+[)]", termino)[0])

	elementos_factorizables_regex = list()
	elementos_factorizables = list()

	for factores in elementos_factorizados:
		if elementos_factorizados.count(factores) > 1 and factores not in elementos_factorizables:
			elementos_factorizables.append(factores)
			factores = r"[\w^]+" + factores.replace("(", "[(]").replace(")", "[)]").replace("+", "[+]").replace("^", r"[\^]")
			elementos_factorizables_regex.append(factores)

	if not elementos_factorizables:
		return expresion

	miniterminos_factorizables = list()
	for elemento_factorizable in elementos_factorizables_regex:
		miniterminos_factorizables.append(re.findall(elemento_factorizable, expresion))

	if not miniterminos_factorizables:
		return expresion

	for parentesis, miniterminos in zip(elementos_factorizables, miniterminos_factorizables):
		ultimo_minitermino = miniterminos[-1]
		for j, minitermino in enumerate(miniterminos):
			if minitermino != ultimo_minitermino:
				minitermino_regex = termino_a_regex(minitermino)
				minitermino_regex = "^" + minitermino_regex + "|[+]" + minitermino_regex

				expresion = re.sub(minitermino_regex, "+", expresion)

			miniterminos[j] = minitermino.replace(parentesis, "")

		reemplazo = f"{parentesis}({'+'.join(miniterminos)})"
		expresion = expresion.replace(ultimo_minitermino, reemplazo)

	expresion = re.sub("[+]+", "+", expresion)

	if expresion.startswith("+"):
		expresion = expresion[1:]

	return expresion


def desarrollar_expresion(expresion: str) -> str:
	if not expresion:
		return ""

	miniterminos = re.findall(r"[\w^]+[(][\w^+]+[)]", expresion)
	for termino in miniterminos:
		elemento_factorizado = re.sub(r"[(][\w^+]+[)]", "", termino)
		productos = termino.replace(elemento_factorizado, "").replace("(", "").replace(")", "").split("+")
		expresiones_desarrolladas = list()
		for producto in productos:
			expresiones_desarrolladas.append(elemento_factorizado + producto)

		expresion = expresion.replace(termino, "+".join(expresiones_desarrolladas))

	maxiterminos = re.findall(r"[(][\w^+]+[)][(][\w^+]+[)]", expresion)
	for maxitermino in maxiterminos:
		factores = maxitermino[1:][:-1].split(")(")
		factores[0] = factores[0].split("+")
		factores[1] = factores[1].split("+")

		terminos_desarrollados = list()
		for factor in factores[0]:
			for factor1 in factores[1]:
				terminos_desarrollados.append(factor + factor1)

		expresion = expresion.replace(maxitermino, "+".join(terminos_desarrollados))

	return expresion


def reducir_f_sop(variables: list, expresion: str, imprimir_f: bool, llamadas=0) -> str:
	# Reduce una expresión SOP cualesquiera usando álgebra de Boole
	# Esta función utiliza:
	#       A+AB = A ; ^A+^AB = ^A
	#       A+^AB = A+B ; ^A+AB = ^A+B
	#       AB+^AB = B(A+^A)
	# 		A+^A = 1

	if llamadas > 5:
		return expresion

	terminos_reducibles = generar_terminos_reducibles(variables)

	if imprimir_f:
		print(utilidades.escribir_como_funcion(variables, expresion))
	else:
		print("Verificando...")

	expresion_org = expresion
	expresion = algebra.ordenar_miniterminos(variables, expresion)
	if expresion_org != expresion:
		utilidades.imprimir_equivalencia(expresion)

	expresion_org = expresion

	while True:
		expresion_de_entrada = expresion
		expresion_anterior = expresion_de_entrada

		expresiones = re.findall(r"[(][\w^+]+[)]", expresion)
		if not expresiones:
			expresion = reducir_a_or_ab(expresion)
			if expresion_anterior != expresion:
				utilidades.imprimir_equivalencia(expresion)
				expresion_anterior = expresion

			expresion = reducir_a_or_not_a_and_b(expresion)
			if expresion_anterior != expresion:
				utilidades.imprimir_equivalencia(expresion)
				expresion_anterior = expresion

			expresion = reducir_terminos(terminos_reducibles, expresion)
			if expresion_anterior != expresion:
				utilidades.imprimir_equivalencia(expresion)
				expresion_anterior = expresion

			expresion = factorizar_expresion(variables, expresion)
			if expresion_anterior != expresion:
				utilidades.imprimir_equivalencia(expresion)
				expresion_anterior = expresion
		else:
			for exp in expresiones:
				input_data = exp.replace("(", "").replace(")", "")
				exp = termino_a_regex(exp)
				expresion_anterior = input_data

				expresion_procesada = reducir_a_or_ab(input_data)
				expresion_procesada = reducir_a_or_not_a_and_b(expresion_procesada)
				expresion_procesada = reducir_terminos(terminos_reducibles, expresion_procesada)
				expresion_procesada = factorizar_expresion(variables, expresion_procesada)
				expresion_procesada = f"({expresion_procesada})"
				expresion = re.sub(exp, expresion_procesada, expresion)

			expresion = reducir_terminos(terminos_reducibles, expresion)
			expresion = factorizar_expresion_factorizada(expresion)

		if expresion_de_entrada == expresion:
			break
		elif expresion_anterior != expresion:
			utilidades.imprimir_equivalencia(expresion)

	expresion_anterior = expresion
	expresion = reducir_terminos(terminos_reducibles, expresion)
	if expresion_anterior != expresion:
		utilidades.imprimir_equivalencia(expresion)
		expresion_anterior = expresion

	while "(" in expresion and not expresion.startswith("("):
		expresion = desarrollar_expresion(expresion)

		if expresion_anterior != expresion:
			utilidades.imprimir_equivalencia(expresion)
			expresion_anterior = expresion
		else:
			break

	expresion_anterior = expresion
	expresion = algebra.ordenar_miniterminos(variables, expresion)
	if expresion_anterior != expresion:
		utilidades.imprimir_equivalencia(expresion)

	if expresion_org == expresion:
		return expresion

	checks_out = logica.comparar_expresiones(variables, expresion_org, expresion)[1]
	if not checks_out:
		raise KeyboardInterrupt("Error al reducir")

	return reducir_f_sop(variables, expresion, False, llamadas + 1)
