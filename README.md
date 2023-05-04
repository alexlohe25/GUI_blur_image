# GUI Procesamiento distribuido

## Integrantes del equipo 
- Fernando Jiménez Pereyra
    - A01734609
- Daniel Munive Meneses
    - A01734205
- Alejandro López Hernández
    - A01733984

# Ejecución de la interfaz

Para ejecutar la interfaz gráfica se requiere primeramente de tener instalados las dependencias, lo cual podría requerir que sean instaladas con el manejador de paquetes de la distribución en vez de pip, ya que la interfaz gráfica requiere correr con privilegios, a su vez que el ejecutable que va a correr el cluster se encuentre en el mismo directorio donde nos encontramos.

Una vez instaladas las dependencias se debe estar posicionado en el directorio /mirror/mpiu/ (este paso es válido para nuestra arquitectura, ya que nuestro ejecutable para el cluster se encuentra en este directorio)

Antes de ejecutar la interfaz debemos comprobar que nuestro usuario cuente con un display, para hacerlo únicamente tendremos que ejecutar el comando “echo $DISPLAY”, en caso de retornar cualquier display podemos seguir con ejecución de la interfaz, en caso de no retornar nada tendremos que cambiarnos a un usuario que si posea display. Esta es la razón por la que nuestra interfaz hace uso de privilegios, debido a que el usuario mpiu necesario para ejecutar el procesamiento en el cluster no posee un display, por lo que corremos la interfaz con con privilegios para cambiar internamente de usuario.
