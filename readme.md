# Servicio web para recortar URLs

## Contenido

- [Servicio web para recortar URLs](#servicio-web-para-recortar-urls)
  - [Contenido](#contenido)
  - [Instalación](#instalación)
  - [REST-API](#rest-api)
    - [Consultar URLs](#consultar-urls)
    - [Agregar nueva URL](#agregar-nueva-url)
    - [Editar URLs](#editar-urls)
    - [Eliminar URLs](#eliminar-urls)


## Instalación

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

## REST-API

### Consultar URLs

**Método:** *GET*

**Ruta:** `<host>/api/`

**Parámetros de URL:**

* `token` (Opcional): Token único de usuario. Cuando no se proporciona un token,
la API devuelve una lista de todas las URLs públicas disponibles. De lo
contrario, la API devuelve la lista de todas las URLs, tanto públicas como
privadas, creadas por dicho usuario.

**Devuelve:**

Un JSON con la lista de URLs con los siguientes campos:

* `id`: ID de la URL.
* `long_url`: URL original.
* `short_url`: URL corta.
* `creator`: Nombre de usuario que creo la URL.
* `is_private`: Un booleano indicando si la URL es privada o no.
* `allow_list`: Lista de usuarios que tienen permitido acceder a la URL cuando
es privada.
* `views`: Número de veces que la URL fue accedida, tanto por usuarios
registrados como invitados.
* `history`: Lista de usuarios registrados que accedieron a la URL.

**Ejemplo:**

**URL:**

`http://127.0.0.1:8000/api/`

**Método:**

GET

**Respuesta:**

```json
[
    {
        "id": 1,
        "long_url": "https://facebook.com",
        "short_url": "127.0.0.1:8000/redirect/gzph2Fgx",
        "creator": null,
        "is_private": false,
        "allow_list": [],
        "views": 2,
        "history": [
            "foobar"
        ]
    },
    {
        "id": 2,
        "long_url": "https://www.google.com",
        "short_url": "127.0.0.1:8000/redirect/mGEpooiD",
        "creator": null,
        "is_private": false,
        "allow_list": [],
        "views": 0,
        "history": []
    },
    {
        "id": 4,
        "long_url": "https://discord.com",
        "short_url": "127.0.0.1:8000/redirect/gwAGhxiI",
        "creator": "vdae",
        "is_private": false,
        "allow_list": [],
        "views": 3,
        "history": [
            "vdae",
            "foobar"
        ]
    }
]
```

**URL:**

`http://127.0.0.1:8000/api/?token=80ae398c-fb2c-40cf-ac5d-fec93ec4dff7`

**Método:**

GET

**Respuesta:**

```json
[
    {
        "id": 3,
        "long_url": "https://www.github.com",
        "short_url": "127.0.0.1:8000/redirect/iVbDdIzi",
        "creator": "vdae",
        "is_private": true,
        "allow_list": [
            "vdae"
        ],
        "views": 0,
        "history": []
    },
    {
        "id": 4,
        "long_url": "https://discord.com",
        "short_url": "127.0.0.1:8000/redirect/gwAGhxiI",
        "creator": "vdae",
        "is_private": false,
        "allow_list": [],
        "views": 3,
        "history": [
            "vdae",
            "foobar"
        ]
    }
]
```

### Agregar nueva URL

**Método:** *POST*

**Ruta:** `<host>/api/`

**Headers:**

* `token` (Opcional): Token único de usuario.

**Body:**

Un JSON con la lista de URLs con los siguientes campos:

* `url`: URL que se desea recortar.
* `is_private`: Un booleano indicando si la URL será privada o no. Se requiere
haber proporcionado antes un token válido.
* `allow_list`: Lista de usuarios que tendrán permitido acceder a la URL. Este
campo es ignorado si `is_private=False`.

**Devuelve:**

Un JSON con la lista de URLs con los siguientes campos:

* `id`: ID de la URL creada.
* `long_url`: URL original.
* `short_url`: URL corta.
* `is_private`: Un booleano indicando si la URL es privada o no.
* `allow_list`: Lista de usuarios que tienen permitido acceder a la URL cuando
es privada.

**Status code:**

* `200`: La operación fue exitosa.
* `401`: Se intentó crear una URL privada sin un token válido.
* `500`: El cuerpo no es un JSON válido o este no está en el formato requerido.

**Ejemplo**

**URL:**

`http://127.0.0.1:8000/api/`

**Método:**

POST

**Headers:**

```
token: 80ae398c-fb2c-40cf-ac5d-fec93ec4dff7
```

**Body:**

```json
[
    {
        "url": "stackoverflow.com/",
        "is_private": false,
        "allow_list": []
    },
    {
        "url": "gmail.com",
        "is_private": true,
        "allow_list": [
            "vdae"
        ]
    }
]
```

**Respuesta:**

```json
[
    {
        "id": 5,
        "long_url": "https://stackoverflow.com/",
        "short_url": "127.0.0.1:8000/redirect/P4iGI23u",
        "is_private": false,
        "allow_list": []
    },
    {
        "id": 6,
        "long_url": "https://gmail.com",
        "short_url": "127.0.0.1:8000/redirect/F85JIDCp",
        "is_private": true,
        "allow_list": [
            "vdae"
        ]
    }
]
```

### Editar URLs

**Método:** *PUT*

**Ruta:** `<host>/api/id/`

**Headers:**

* `token`: Token único de usuario.

**Body:**

Un JSON con los siguientes campos:

* `url` (Opcional): URL que se desea recortar.
* `is_private` (Opcional): Un booleano indicando si la URL será privada o no.
* `allow_list` (Opcional): Lista de usuarios que tendrán permitido acceder a la
URL. Este campo es ignorado si `is_private=False`.

**Status code:**

* `200`: La operación fue exitosa.
* `400`: El ID no corresponde a una URL válida.
* `401`: El usuario no tiene permitido editar la URL.
* `500`: El cuerpo no es un JSON válido o este no está en el formato requerido.

**Ejemplo:**

**URL:**

`http://127.0.0.1:8000/api/4`

**Método:**

PUT

**Headers:**

```
token: 80ae398c-fb2c-40cf-ac5d-fec93ec4dff7
```

**Body:**

```json
{
    "is_private": true,
    "allow_list": [
        "vdae"
    ]
}
```


### Eliminar URLs

**Método:** *DELETE*

**Ruta:** `<host>/api/id/`

**Headers:**

* `token`: Token único de usuario.

**Status code:**

* `200`: La operación fue exitosa.
* `400`: El ID no corresponde a una URL válida.
* `401`: El usuario no tiene permitido eliminar la URL.

**Ejemplo:**

**URL:**

`http://127.0.0.1:8000/api/4`

**Método:**

DELETE