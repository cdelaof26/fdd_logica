import herramientas.recuadro as recuadro
import herramientas.utilidades as utilidades
import herramientas.logica as logica

menu = recuadro.crear_recuadro(
    ["    Bienvenido a FDD-lógica",
     "  Menu",
     # "1. Crear circuito",
     "1. Crear tabla de verdad",
     "2. Crear tabla de verdad de expresión",
     # "4. Reducir expresión",
     # "5. Expandir expresión",
     # "M. Manejar circuitos",
     "S. Salir"]
)

while True:
    try:
        print(menu)
        print("Selecciona una opción")
        seleccion = utilidades.seleccionar_opcion(["1", "2", "3", "4", "S"])

        if seleccion == "1":
            print(recuadro.crear_tabla(logica.crear_tabla_de_verdad()))

        if seleccion == "2":
            print(recuadro.crear_tabla(logica.deducir_tabla_de_verdad()))

        if seleccion == "S":
            break

        input("  Presiona enter para continuar ")
        utilidades.limpiar_pantalla()
    except KeyboardInterrupt:
        print("\n    Proceso interrumpido!")
        input("  Presiona enter para continuar ")
        utilidades.limpiar_pantalla()

print("Bye")
