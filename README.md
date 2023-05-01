# fdd_logica

### ¿Qué es esto?

Un proyecto básico para el procesamiento de funciones booleanas

### Descargo de responsabilidad

Este proyecto se creó con fines educativos

Antes de utilizarlo, por favor lee la [LICENCIA](LICENSE)

### Dependencias

1. Python 3.6 ó superior


### Ejecutar proyecto

Clona este repositorio

<pre>
$ git clone https://github.com/cdelaof26/fdd_logica.git
</pre>

Ingresa a la carpeta del proyecto

<pre>
$ cd fdd_logica
</pre>

Ejecútalo

<pre>
# Si te encuentras en macOS ó Linux
$ python3 main.py

# Si te encuentras en Windows
$ python main.py
</pre>


### Changelog

### v0.0.5
- Agregado `Reducir expresión` por medio de algebra de Boole
  - El soporte es limitado y exclusivo para expresiones de tipo SOP,
    es posible que no se agregue soporte para otro tipo de funciones
    en un futuro debido a la complejidad de las reducciones.
  - **Los resultados arrojados por esta función muchas veces son 
    reducibles**


### v0.0.4
- Agregado `Deducir expresión de tabla de verdad`
- Agregado `Expandir expresión`
  - Por ahora solo procesa expresiones SOP y POS, el soporte
    para expresiones de otro tipo se agregará después
- Los circuitos creados se guardarán automáticamente
- Cambio en la detección de funciones booleanas SOP


### v0.0.3
- Mejora en la experiencia de uso
- Agregado `Crear circuito`
- Agregado `Clasificar expresión`


### v0.0.2
- Mejora en la experiencia de uso


### v0.0.1
- Proyecto inicial
