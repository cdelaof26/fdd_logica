import herramientas.utilidades as utilidades
import herramientas.logica as logica

# Utilidades para la operación "algebraica" de expresiones

"""
	# Reglas básicas

A_OR_0           = "A+0=A"
A_OR_1           = "A+1=1"
A_AND_0          = "A*0=0"
A_AND_1          = "A*1=A"
A_OR_A           = "A+A=A"
A_OR_NOT_A       = "A+^A=1"          <--- SOP_C
A_AND_A          = "A*A=A"
A_AND_NOT_A      = "A*^A=0"

NOT_NOT_A        = "^^A=A"
A_OR_A_AND_B     = "A+AB=A"
A_OR_NOT_A_AND_B = "A+^AB=A+B"
(A_OR_B)(A_OR_C) = "(A+B)(A+C)=A+BC" <--- POS_C
NOT_(A_AND_B)    = "^(A*B)=^A+^B"
NOT_(A_OR_B)     = "^(A+B)=^A^B"
"""


def obtener_t_no_c_de_sop(variables: list, expresion: str) -> tuple:
	terminos = expresion.split("+")
	terminos_no_canonicos = list()

	for termino in terminos:
		if not utilidades.cadena_contiene_lista_n_veces(termino, variables, 1):
			terminos_no_canonicos.append(termino)

	return terminos, terminos_no_canonicos


def expandir_termino_sop(termino: str, variables: list) -> str:
	# Se utiliza la regla del algebra de Boole que dice
	#   A+^A=1

	for variable in variables:
		if variable in termino:
			continue

		print(f"\nExpandiendo \"{termino}\"")
		print(f"->  {termino}({variable}+^{variable})")
		print(f" = {termino}{variable}+{termino}^{variable}")

		return expandir_termino_sop(
			f"{termino}{variable}", variables
		) + "+" + expandir_termino_sop(f"{termino}^{variable}", variables)

	return termino


def ordenar_minitermino(termino: str, variables: list) -> str:
	termino_ordenado = ""
	for variable in variables:
		# Se considera que no existe la misma variable en
		# un mismo término de forma "normal" y complementada
		# Puede que aquí haya un punto de fallo...
		#
		if f"^{variable}" in termino:
			termino_ordenado += f"^{variable}"
			continue

		if variable in termino:
			termino_ordenado += f"{variable}"

	return termino_ordenado


def expandir_f_sop(variables: list, expresion: str) -> str:
	# Expande una expresión SOP a SOP canónica

	terminos, terminos_no_canonicos = obtener_t_no_c_de_sop(variables, expresion)

	for termino in terminos_no_canonicos:
		termino_expandido = expandir_termino_sop(termino, variables)
		terminos[terminos.index(termino)] = termino_expandido
		print()

	# Quizá requiera buscar otra solución para quitar duplicados...
	expresion = "+".join(terminos)

	terminos = list()
	for termino in expresion.split("+"):
		terminos.append(ordenar_minitermino(termino, variables))

	return "+".join(utilidades.filtrar_duplicados_en(terminos))


def obtener_t_no_c_de_pos(variables: list, expresion: str) -> tuple:
	terminos = expresion.split(")(")
	terminos_no_canonicos = list()

	for i, termino in enumerate(terminos):
		if not utilidades.cadena_contiene_lista_n_veces(termino, variables, 1):
			terminos_no_canonicos.append(termino.replace("(", "").replace(")", ""))
		terminos[i] = termino.replace("(", "").replace(")", "")

	return terminos, terminos_no_canonicos


def expandir_termino_pos(termino: str, variables: list) -> str:
	# Se utiliza la regla del algebra de Boole que dice
	#   (A+B)(A+C)=A+BC
	# Donde
	# 		A es término
	# 		B la variable faltante
	# 		C la variable faltante complementada

	for variable in variables:
		if variable in termino:
			continue

		print(f"\nExpandiendo \"{termino}\"")
		print(f"-> ({termino})+{variable}^{variable}")
		print(f" = ({termino}+{variable})({termino}+^{variable})")

		return expandir_termino_pos(
			f"{termino}+{variable}", variables
		) + ")(" + expandir_termino_pos(f"{termino}+^{variable}", variables)

	return termino


def ordenar_maxitermino(termino: str, variables: list) -> str:
	termino_ordenado = ""
	for variable in variables:
		# Se considera que no existe la misma variable en
		# un mismo término de forma "normal" y complementada
		# Puede que aquí haya un punto de fallo...
		#
		if f"^{variable}" in termino:
			termino_ordenado += f"^{variable}+"
			continue

		if variable in termino:
			termino_ordenado += f"{variable}+"

	return termino_ordenado[:-1]


def expandir_f_pos(variables: list, expresion: str) -> str:
	# Expande una expresión POS a POS canónica

	terminos, terminos_no_canonicos = obtener_t_no_c_de_pos(variables, expresion)

	for termino in terminos_no_canonicos:
		termino_expandido = expandir_termino_pos(termino, variables)
		terminos[terminos.index(termino)] = termino_expandido
		print()

	expresion = ")(".join(terminos)

	terminos = list()
	for termino in expresion.split(")("):
		terminos.append(ordenar_maxitermino(termino, variables))

	return "(" + ")(".join(utilidades.filtrar_duplicados_en(terminos)) + ")"


def expandir_funcion() -> str:
	utilidades.limpiar_pantalla()

	variables, expresion = logica.obtener_funcion_booleana()
	tipo = logica.clasificar_expresion(variables, expresion)

	utilidades.limpiar_pantalla()

	if tipo == logica.FuncionLogica.NA:
		return "Aún no esta implementada la funcionalidad para expandir funciones cualesquiera"
	elif tipo == logica.FuncionLogica.SOP_C:
		return "La función ya está en forma SOP canónica"
	elif tipo == logica.FuncionLogica.POS_C:
		return "La función ya está en forma POS canónica"

	print(utilidades.escribir_como_funcion(variables, expresion))

	if tipo == logica.FuncionLogica.SOP:
		return utilidades.escribir_como_funcion(variables, expandir_f_sop(variables, expresion))

	return utilidades.escribir_como_funcion(variables, expandir_f_pos(variables, expresion))
