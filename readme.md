# Instalación

1. Crear un entorno virtual llamado `shorturl`.

```bash
python -m env shorturl
cd shorturl
./Scripts/activate
```

2. El siguiente servicio web hace uso de Django y MySQL, por lo que es
necesario instalarlo en caso de que no lo esté.

```bash
python -m pip install Django
python -m pip install mysql
```

3. Descargar y guardar el contenido de este repositorio en el entorno recién
creado.

```
> shorturl
    > Include
    > Lib
    > Scripts
    > shorturl
        > app
        > shorturl
            > settings.py
            ...
        > manage.py
        > readme.md
    ...
```
4. Configurar los datos de la conexión a MySQL en el archivo `settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'shorturl',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'LOCALHOST',
        'PORT': 3306
    }
}
```

6. Iniciar el servicio web.

```bash
cd shorturl
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```