from django.http import HttpResponse
from . import models

import json
import random
import string


"""
Devuelve el user_id asociado a un token.
"""
def find_user_id(token):
    if token is None:
        return None
    try:
        return models.UserTokens.objects.get(token=token).user_id
    except models.UserTokens.DoesNotExist:
        return None


"""
Genera un string aleatorio.
"""
def random_string(length):
    return "".join(random.choices(string.ascii_letters + string.digits,
                   k=length))


"""
GET request. Devuelve la lista de URLs creadas por un usuario.
"""
def GET(request):
    token = request.GET.get("token", default=None)
    creator_id = find_user_id(token)
    response = []
    if token is None or creator_id is not None:
        for item in models.URLs.objects.filter(creator_id=creator_id):
            response.append({
                'id': item.id,
                'long_url': item.long_url,
                'short_url': request.get_host() + "/redirect/" + item.short_url,
                'is_private': item.is_private
            })
    return HttpResponse(json.dumps(response), content_type="application/json")


"""
POST request. Genera una lista de URLs cortas a partir de URLs largas.
Ver documentación para conocer más detalles sobre el formato del header, body y
response.
"""
def POST(request):
    token = request.headers.get("Authorization", default=None)
    creator_id = find_user_id(token)

    try:
        body = json.loads(request.body)
    except ValueError:
        return HttpResponse("JSON malformed", status=500)

    if not isinstance(body, list):
        return HttpResponse(
            "JSON does not follow the required format", status=500
        )

    try:
        response = []
        for item in body:
            long_url = item['url']
            if not long_url.startswith("https://"):
                long_url = "https://" + long_url
            short_url = random_string(length=8)
            is_private = item['is_private']
            if is_private and creator_id is None:
                return HttpResponse(
                    "Cannot create private URLs without valid token", status=401
                )

            entry = models.URLs(
                long_url=long_url,
                short_url=short_url,
                creator_id=creator_id,
                is_private=is_private
            )
            entry.save()
            response.append({
                'id': entry.id,
                'long_url': long_url,
                'short_url': request.get_host() + "/redirect/" + short_url,
                'is_private': is_private
            })
    except KeyError:
        return HttpResponse(
            "JSON does not follow the required format", status=500
        )

    return HttpResponse(json.dumps(response),
                        content_type="application/json",
                        status=200)


"""
PUT request. Edita una URL creada por un usuario.
"""
def PUT(request, id):
    token = request.headers.get("Authorization", default=None)
    creator_id = find_user_id(token)

    try:
        body = json.loads(request.body)
    except ValueError:
        return HttpResponse("JSON malformed", status=500)

    if not isinstance(body, dict):
        return HttpResponse(
            "JSON does not follow the required format", status=500
        )

    try:
        entry = models.URLs.objects.get(id=id)
        if creator_id is None or entry.creator_id != creator_id:
            return HttpResponse("Permission denied", status=401)

        if 'url' in body:
            entry.long_url = body['url']
        if 'is_private' in body:
            entry.is_private = body['is_private']
        entry.save()

        return HttpResponse("Sucess", status=200)
    except models.URLs.DoesNotExist:
        return HttpResponse("Invalid url id", status=400)


"""
DELETE request. Elimina una URL creada por un usuario.
"""
def DELETE(request, id):
    token = request.headers.get("Authorization", default=None)
    creator_id = find_user_id(token)
    try:
        entry = models.URLs.objects.get(id=id)
        if creator_id is None or entry.creator_id != creator_id:
            return HttpResponse("Permission denied", status=401)
        entry.delete()
        return HttpResponse("Success", status=200)
    except:
        return HttpResponse("Invalid url id", status=400)


"""
Rest-API para solicitudes GET y POST.
"""
def makeURL(request):
    if request.method == "GET":
        return GET(request)
    elif request.method == "POST":
        return POST(request)
    else:
        return HttpResponse("Unknown request")


"""
Rest-API para solicitudes PUT y DELETE.
"""
def editURL(request, id):
    if request.method == "PUT":
        return PUT(request, id)
    if request.method == "DELETE":
        return DELETE(request, id)
    else:
        return HttpResponse("Unknown request")
