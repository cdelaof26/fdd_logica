import herramientas.recuadro as recuadro
import herramientas.utilidades as utilidades
import herramientas.logica as logica
import herramientas.circuitos as circuitos

# circuitos.mapear_circuito()

while True:
    print(recuadro.crear_recuadro(
            ["  Menu",
             "1. Crear tabla de verdad",
             "2. Crear tabla de verdad de expresión",
             # "3. Reducir expresión",
             "S. Salir"]
        )
    )

    print("Selecciona una opción")
    seleccion = utilidades.seleccionar_opcion(["1", "2", "S"])

    if seleccion == "1":
        print(recuadro.crear_tabla(logica.crear_tabla_de_verdad()))

    if seleccion == "2":
        print(recuadro.crear_tabla(logica.deducir_tabla_de_verdad()))

    if seleccion == "2":
        pass

    if seleccion == "S":
        break

print("Bye")
