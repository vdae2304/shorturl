from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . import models
from . import forms

import json
import random
import string


"""
Página de inicio que verá el usuario al ingresar al sitio.
"""
def indexView(request):
    username = request.user.username if request.user.is_authenticated else ""
    return render(request, 'index.html', context={
        'username': username
    })


"""
Formulario para iniciar sesión.
"""
def loginView(request):
    if not request.user.is_authenticated:
        form = forms.LoginForm()
        login_fail = request.GET.get('login_fail', default=0)
        return render(request, 'login.html', context={
            'form': form,
            'login_fail': login_fail
        })
    else:
        return redirect("/index/")


"""
Respuesta al formulario de inicio de sesión. Autentifica los datos de inicio.
"""
def authView(request):
    form = forms.LoginForm(request.POST)
    if not form.is_valid():
        return redirect("/index/")
    username = form.cleaned_data["username"]
    password = form.cleaned_data["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("/index/")
    else:
        return redirect("/login?login_fail=1")


"""
Finaliza la sesión del usuario.
"""
def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("/index/")


"""
Formulario para registrar nuevo usuario.
"""
def signUpView(request):
    form = forms.SignUpForm()
    username_in_use = request.GET.get("username_in_use", 0)
    email_used = request.GET.get("email_in_use", 0)
    password_mismatch = request.GET.get("password_mismatch", 0)
    return render(request, 'signup.html', context={
        'form': form,
        'username_in_use': username_in_use,
        'email_in_use': email_used,
        'password_mismatch': password_mismatch
    })


"""
Respuesta al formulario de registro de usuario. Crea un nuevo usuario.
"""
def registerView(request):
    form = forms.SignUpForm(request.POST)
    if not form.is_valid():
        return redirect("/index/")
    username = form.cleaned_data["username"]
    email = form.cleaned_data["email"]
    password = form.cleaned_data["password"]
    confirm_password = form.cleaned_data["confirm_password"]
    if User.objects.filter(username=username).count() > 0:
        return redirect("/sign-up?username_in_use=1")
    if User.objects.filter(email=email).count() > 0:
        return redirect("/sign-up?email_in_use=1")
    if password != confirm_password:
        return redirect("/sign-up?password_mismatch=1")
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    user.save()
    return redirect("/index/")


def random_string(length):
    return "".join(random.choices(string.ascii_letters + string.digits,
                                  k=length))

def makeURLView(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            response = []
            for item in body["URLs"]:
                url = item["URL"]
                if not url.startswith("https://"):
                    url = "https://" + url
                isPrivate = item["isPrivate"]
                shorturl = random_string(10)
                token = random_string(20) if isPrivate else ""
                newURL = models.ShortURLs(
                    url=url,
                    shorturl=shorturl,
                    creator=0,
                    token=token
                )
                newURL.save()
                response.append({
                    "longURL": url,
                    "shortURL": request.get_host() + "/redirect/" + shorturl,
                    "token": token
                })
            response = {"URLs": response}
            response = json.dumps(response)
            return HttpResponse(response, content_type='application/json')
        except KeyError:
            return HttpResponse("JSON malformed", status=500)
    return HttpResponse("Hola mundo")


"""
Redirige a la URL larga. Si no existe una URL asociada, redirige a /index/.
"""
def redirectView(request, short_url):
    try:
        entry = models.ShortURLs.objects.get(shorturl=short_url)
        return redirect(entry.url)
    except models.ShortURLs.DoesNotExist:
        return redirect("/index/")
