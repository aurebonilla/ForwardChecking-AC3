# Forward Checking y AC3 para Crucigramas

Este proyecto implementa un juego de crucigramas utilizando los algoritmos de Forward Checking (FC) y AC3 para resolver el crucigrama. La interfaz gráfica está construida con `pygame` y `tkinter`.

## Estructura del Proyecto

El proyecto está compuesto por los siguientes archivos:

- `main.py`: Contiene la lógica principal del programa, incluyendo la interfaz gráfica y la implementación de los algoritmos FC y AC3.
- `dominio.py`: Define la clase `Dominio`, que representa un conjunto de palabras de una longitud específica.
- `variable.py`: Define la clase `Variable`, que representa una palabra potencial en el crucigrama.
- `tablero.py`: Define la clase `Tablero`, que representa el estado del crucigrama.

## Requisitos

- Python 3.x
- Pygame
- Tkinter

Puedes instalar `pygame` utilizando pip:

```sh
pip install pygame
```
## Uso
### Ejecución del Programa
Para ejecutar el programa, simplemente corre el archivo main.py:
```sh
python main.py
```
### Interacción con la Interfaz

- Botón FC: Ejecuta el algoritmo de Forward Checking para intentar resolver el crucigrama.

- Botón AC3: Ejecuta el algoritmo AC3 para reducir los dominios de las variables y luego intenta resolver el crucigrama.

- Botón Reset: Resetea el tablero y limpia las variables.

- Clic Izquierdo en el Tablero: Marca una celda como ocupada (*).

- Clic Derecho en el Tablero: Permite introducir un carácter en una celda específica.

## Algoritmos Implementados
### Forward Checking (FC)
El algoritmo de Forward Checking se utiliza para intentar resolver el crucigrama verificando las restricciones hacia adelante.

### AC3
El algoritmo AC3 se utiliza para reducir los dominios de las variables antes de intentar resolver el crucigrama.

### Ejemplo de Uso
1. Ejecuta el programa.
2. Marca las celdas ocupadas en el tablero.
3. Pulsa el botón AC3 para reducir los dominios.
4. Pulsa el botón FC para intentar resolver el crucigrama.
5. Si es necesario, resetea el tablero y vuelve a intentarlo.