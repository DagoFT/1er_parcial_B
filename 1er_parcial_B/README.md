# Paint App con Arcade

Este proyecto es una aplicación de dibujo tipo Paint desarrollada en Python usando la librería **Arcade**. Permite dibujar con diferentes herramientas, cambiar colores, borrar, y guardar/cargar dibujos en formato JSON.

## Estructura de archivos

project/
├─ main.py       Archivo principal con la lógica del programa y GUI  
├─ tool.py       Definición de herramientas (Pencil, Marker, Spray, Eraser)  
└─ README.md     Este archivo  

## Requisitos

- Python 3.10 o superior  
- Librerías de Python:
  - arcade
  - tkinter (incluido por defecto en Python)
  - json (incluido por defecto en Python)

Instalación de Arcade:

pip install arcade

## Herramientas disponibles

PENCIL: Dibujo fino con línea delgada  
MARKER: Línea gruesa para trazos destacados  
SPRAY: Efecto spray con dispersión de puntos  
ERASER: Borrar partes del dibujo

## Colores disponibles

Los colores iniciales disponibles en la barra lateral son:

Negro  
Rojo  
Azul  
Verde  
Amarillo  
Naranja  
Rosa  
Púrpura  
Cian  
Marrón  
Gris  
Lima  

## Uso

Ejecutar el programa:

python main.py

La interfaz de la aplicación incluye:

- Barra lateral con herramientas y colores  
- Área de dibujo principal  
- Indicaciones de teclado para guardar y cargar  

### Atajos de teclado

1 → Seleccionar Pencil  
2 → Seleccionar Marker  
3 → Seleccionar Spray  
4 → Seleccionar Eraser  
A, S, D, F → Cambiar entre colores predefinidos  
O → Guardar dibujo (se puede ingresar un nombre)  
L → Cargar dibujo desde un archivo JSON  

## Guardar y cargar

Al presionar O, se abre un diálogo para ingresar el nombre del archivo y guardar el dibujo en formato JSON.  
Al presionar L, se abre un diálogo para seleccionar un archivo JSON previamente guardado.  

## Cómo agregar colores adicionales

Para añadir más colores, edita la lista COLOR_SWATCHES en main.py:

COLOR_SWATCHES = [
    arcade.color.BLACK,
    arcade.color.RED,
    arcade.color.BLUE,
    arcade.color.GREEN,
    arcade.color.YELLOW,
    arcade.color.ORANGE,
    arcade.color.PINK,
    arcade.color.PURPLE,
    arcade.color.CYAN,
    arcade.color.BROWN,
    arcade.color.GRAY,
    arcade.color.LIME,
]

## Licencia

Este proyecto es de uso educativo y libre distribución.
