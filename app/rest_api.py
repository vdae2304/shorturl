from django.http import HttpResponse
from django.contrib.auth.models import User
from . import models

import json
import random
import string


"""
Devuelve el user_id asociado a un token.
"""
def find_userid_by_token(token):
    if token is None:
        return None
    try:
        return models.UserTokens.objects.get(token=token).user_id
    except models.UserTokens.DoesNotExist:
        return None


"""
Devuelve el historial de visualizaciones de una URL.
"""
def get_url_history_visualization(url_id):
    queryset = models.URLVisualizations.objects.filter(url_id=url_id)
    views = queryset.count()
    history = []
    for item in queryset.exclude(user_id__isnull=True):
        username = User.objects.get(id=item.user_id).username
        history.append(username)
    return views, history


"""
Devuelve la lista de usuarios que tienen permitido acceder a una URL privada.
"""
def get_url_allow_list(url_id):
    allow_list = []
    for item in models.URLAllowList.objects.filter(url_id=url_id):
        username = User.objects.get(id=item.user_id).username
        allow_list.append(username)
    return allow_list


"""
GET request. Devuelve la lista de URLs creadas por un usuario.
"""
def GET(request):
    token = request.GET.get("token", default=None)
    creator_id = find_userid_by_token(token)
    response = []
    # Si no hay token, devuelve todas las URLs públicas.
    if token is None:
        for item in models.URLs.objects.filter(is_private=False):
            creator = None
            if item.creator_id is not None:
                creator = User.objects.get(id=item.creator_id).username
            views, history = get_url_history_visualization(item.id)
            response.append({
                'id': item.id,
                'long_url': item.long_url,
                'short_url': request.get_host() + "/" + item.short_url,
                'creator': creator,
                'is_private': item.is_private,
                'allow_list': [],
                'views': views,
                'history': history
            })
    # De lo contrario, devuelve todas las URLs, tanto públicas como privadas,
    # creadas por dicho usuario.
    elif creator_id is not None:
        for item in models.URLs.objects.filter(creator_id=creator_id):
            creator = User.objects.get(id=item.creator_id).username
            allow_list = []
            if item.is_private:
                allow_list = get_url_allow_list(item.id)
            views, history = get_url_history_visualization(item.id)
            response.append({
                'id': item.id,
                'long_url': item.long_url,
                'short_url': request.get_host() + "/" + item.short_url,
                'creator': creator,
                'is_private': item.is_private,
                'allow_list': allow_list,
                'views': views,
                'history': history
            })
    return HttpResponse(json.dumps(response), content_type="application/json")


"""
Genera un string aleatorio.
"""
def random_string(length):
    return "".join(random.choices(string.ascii_letters + string.digits,
                   k=length))


"""
Establece la lista de usuarios que tienen permitido acceder a una URL privada.
"""
def set_url_allow_list(url_id, allow_list):
    models.URLAllowList.objects.filter(url_id=url_id).delete()
    for username in allow_list:
        try:
            user_id = User.objects.get(username=username).id
            entry = models.URLAllowList(url_id=url_id, user_id=user_id)
            entry.save()
        except User.DoesNotExist:
            pass


"""
POST request. Genera una lista de URLs cortas a partir de URLs largas.
Ver documentación para conocer más detalles sobre el formato del header, body y
response.
"""
def POST(request):
    token = request.headers.get("Authorization", default=None)
    creator_id = find_userid_by_token(token)
    # Valida que el cuerpo contenga un JSON válido.
    try:
        body = json.loads(request.body)
    except ValueError:
        return HttpResponse("JSON malformed", status=500)
    if not isinstance(body, list):
        return HttpResponse(
            "JSON does not follow the required format", status=500
        )
    # Itera sobre cada URL en el body.
    try:
        response = []
        for item in body:
            # Las URLs deben comenzar con https://
            long_url = item['url']
            if not long_url.startswith("https://"):
                long_url = "https://" + long_url
            # Genera una URL corta de forma aleatoria.
            short_url = random_string(length=8)
            # Si la URL es privada, debe existir un token válido.
            is_private = item['is_private']
            if is_private and creator_id is None:
                return HttpResponse(
                    "Cannot create private URLs without valid token", status=401
                )
            # Si la URL es privada, debe proporcionarse una lista de usuarios
            # permitidos.
            allow_list = []
            if is_private:
                allow_list = list(item['allow_list'])
            # Crea la URL.
            entry = models.URLs(
                long_url=long_url,
                short_url=short_url,
                creator_id=creator_id,
                is_private=is_private
            )
            entry.save()
            set_url_allow_list(entry.id, allow_list)
            response.append({
                'id': entry.id,
                'long_url': long_url,
                'short_url': request.get_host() + "/" + short_url,
                'is_private': is_private,
                'allow_list': allow_list
            })
    except KeyError:
        return HttpResponse(
            "JSON does not follow the required format", status=500
        )
    # Respuesta del servidor.
    return HttpResponse(json.dumps(response),
                        content_type="application/json",
                        status=200)


"""
PUT request. Edita una URL creada por un usuario.
"""
def PUT(request, id):
    token = request.headers.get("Authorization", default=None)
    creator_id = find_userid_by_token(token)
    # Valida que el cuerpo contenga un JSON válido.
    try:
        body = json.loads(request.body)
    except ValueError:
        return HttpResponse("JSON malformed", status=500)
    if not isinstance(body, dict):
        return HttpResponse(
            "JSON does not follow the required format", status=500
        )
    # Valida que el usuario tenga permisos para editar la URL.
    try:
        entry = models.URLs.objects.get(id=id)
    except models.URLs.DoesNotExist:
        return HttpResponse("Invalid url id", status=400)
    if creator_id is None or entry.creator_id != creator_id:
        return HttpResponse("Permission denied", status=401)
    # Se intentó editar la URL larga.
    if 'url' in body:
        if not body['url'].startswith("https://"):
            body['url'] = "https://" + body['url']
        entry.long_url = body['url']
    # Se intentó editar la privacidad de la URL.
    if 'is_private' in body:
        if body['is_private'] and 'allow_list' in body:
            allow_list = body['allow_list']
            set_url_allow_list(entry.id, allow_list)
        entry.is_private = body['is_private']
    # Guarda los cambios.
    entry.save()
    return HttpResponse("Sucess", status=200)


"""
DELETE request. Elimina una URL creada por un usuario.
"""
def DELETE(request, id):
    token = request.headers.get("Authorization", default=None)
    creator_id = find_userid_by_token(token)
    # Verifica que el usuario tenga permisos para eliminar la URL.
    try:
        entry = models.URLs.objects.get(id=id)
    except:
        return HttpResponse("Invalid url id", status=400)
    if creator_id is None or entry.creator_id != creator_id:
        return HttpResponse("Permission denied", status=401)
    # Elimina la URL.
    entry.delete()
    return HttpResponse("Success", status=200)


"""
Rest-API para solicitudes GET y POST.
"""
def makeURL(request):
    if request.method == "GET":
        return GET(request)
    elif request.method == "POST":
        return POST(request)
    else:
        return HttpResponse("Unknown request", status=404)


"""
Rest-API para solicitudes PUT y DELETE.
"""
def editURL(request, id):
    if request.method == "PUT":
        return PUT(request, id)
    if request.method == "DELETE":
        return DELETE(request, id)
    else:
        return HttpResponse("Unknown request", status=404)
