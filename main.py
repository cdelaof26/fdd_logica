import herramientas.recuadro as recuadro
import herramientas.utilidades as utilidades
import herramientas.logica as logica
import herramientas.circuitos as circuitos

menu = recuadro.crear_recuadro(
    ["    Bienvenido a FDD-lógica",
     "  Menu",
     "1. Crear circuito",
     "2. Clasificar expresión",
     "3. Crear tabla de verdad",
     "4. Deducir tabla de verdad de expresión",
     # "4. Reducir expresión",
     # "5. Expandir expresión",
     # "M. Manejar circuitos",
     "S. Salir"]
)

circuitos_guardados = list()

while True:
    try:
        print(menu)
        print("Selecciona una opción")
        seleccion = utilidades.seleccionar_opcion(["1", "2", "3", "4", "5", "M", "S"])

        if seleccion == "1":
            circuitos_guardados.append(circuitos.crear_circuito())
            print(circuitos_guardados[-1].a_cadena())

        if seleccion == "2":
            utilidades.limpiar_pantalla()
            variables, expresion = logica.obtener_funcion_booleana()
            print("La función es", logica.clasificar_expresion(variables, expresion).a_cadena())

        if seleccion == "3":
            print(recuadro.crear_tabla(logica.crear_tabla_de_verdad()))

        if seleccion == "4":
            print(recuadro.crear_tabla(logica.deducir_tabla_de_verdad()))

        if seleccion == "4":
            pass

        if seleccion == "5":
            pass

        if seleccion == "M":
            pass

        if seleccion == "S":
            break

        input("  Presiona enter para continuar ")
        utilidades.limpiar_pantalla()
    except KeyboardInterrupt:
        print("\n    Proceso interrumpido!")
        input("  Presiona enter para continuar ")
        utilidades.limpiar_pantalla()

print("Bye")
