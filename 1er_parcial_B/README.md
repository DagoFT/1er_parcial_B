# Infografia - Universidad Privada Boliviana 1er parcial B

## Descripción

Este repositorio contiene el código base para el proyecto de tipo B.

Este proyecto implementa la funcionalidad base una versión inicial de PAINT. El proyecto contiene código para la mecánica fundamental y los objetos necesarios. Usted deberá completar el código fuente e implementar funcionalidades adicionales.

## Instrucciones

Para ejecutar el programa de arcade:

1. Clone (o forkee) el repositorio en un directorio local.
2. Abra la carpeta completa con Visual Studio code.
3. Ejecute el archivo main.py.

Siga las instrucciones para la implementación de la evaluación.

### Implementación de características adicionales

La aplicación cuenta con una herramienta de lápiz implementada. El mecanismo de funcionamiento está basado en un conjunto de trazos. El objeto self.traces es una lista de diccionarios, cada elemento representa un trazo a dibujar en la pantalla. Cada trazo tiene el siguiente formato como diccionario de python:
```python
{"tool": TOOL_NAME, "color": COLOR, "trace":[(x0, y0), (x1, y1), ... (xn, yn)]}
```
Usted deberá implementar las siguientes características como nuevas clases en el archivo `tool.py`:

#### Marker Tool

La herramienta de marcador funciona similar a la herramienta del lápiz, pero en este caso se cuenta con un grosor incrementado.

#### Spray Tool

La herramienta de spray deberá pintar cierto número de pixeles alrededor del pixel en el que se hace clic.

#### Eraser Tool

La herramienta borrador, deberá eliminar los trazos que toca.

#### Guardado y Carga de dibujos

Adicionalmente, usted deberá implementar una funcionalidad de Guardado y Carga de dibujos simplemente guardando el objeto `self.traces` en un archivo de texto.
El guardado deberá realizarse al presionar la tecla `O` y la carga podrá realizarse a través de un argumento de línea de comandos.
Para la carga deberá usar la siguiente forma de invocar el programa:

```bash
python main.py ruta/a/mi/archivo
```


#### (Extra) Interfaz gráfica

Se considerará la implementación de una interfaz gráfica con botones para cambiar herramientas y colores y cualquier adición de funcionalidad al programa.

### Envío del código

Usted deberá enviar un enlace a un repositorio de github que solamente contendrá el código del proyecto en cuestión. Se recomienda que, para salvar inconvenientes con GIT, usted realice un fork de este repositorio en su propia cuenta, y luego clone el fork a su directorio local. 

Una vez finalizadas las tareas, se deberá enviar un email por grupo con los siguientes datos:

 - Destinatario: eduardo.laruta+tareas@gmail.com
 - Asunto: 1era Evaluacion parcial Infografia
 - Contenido: Nombres y códigos de los integrantes y el enlace al repositorio de GitHub
