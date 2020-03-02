# Proyecto General Ingenieria de Software
- ALEX DARIO MACAS ALCOCER
- ROBERTO MENA
- ANTHONY HERRERA
- GAMBAROTTI

# Pasos para installar los plugins que se necesitan
Ir al directorio de la aplicacion '../educacion-continua-1/edc1'
Ejecutar el comando:
    pip install -r requirements.txt

# Configuraciones para la database
Ir al directorio de la aplicacion 'educacion-continua-1/edc1/edc1'
En el archivo setting.py en la seccion DATABASE
Crear en su equipo la database en postgreSql con el mismo nombre del campo NAME
En el campo PASSWORD colocar su contraseña

# Pasos para migrar los models a la database
Ir al directorio de la aplicacion '../educacion-continua-1/edc1'
Ejecutar el comando
    python manage.py makemigrations
    python manage.py migrate

# Pasos para ejecutar la app
Ir al directorio de la aplicacion '../educacion-continua-1/edc1'
Ejecutar el comando:
    python manage.py runserver

# Pasos para crear nueva app
1. `python manage.py startapp <nombre_app>`
2. Mover la carpeta de la nueva app a la carpeta `edc1\apps_academico`
3. Agregar la nueva app en `edc1\edc1\settings.py` 
4. Agregar un archivo `urls.py` a la carpeta de la nueva app con el cotenido:
    ```
        urlpatterns = []
    ```
5. Hacer referencia a este `urls.py` desde `edc1\edc1\urls.py`

