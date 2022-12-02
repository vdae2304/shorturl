from django.shortcuts import redirect, render

from django.contrib import auth
from django.contrib.auth.models import User

from . import forms
from . import models


"""
Página de inicio que verá el usuario al ingresar al sitio.
"""
def indexView(request):
    if request.user.is_authenticated:
        username = request.user.username
        token = models.UserTokens.objects.get(user_id=request.user.id).token
    else:
        username = ""
        token = ""
    return render(request, 'index.html', context={
        'username': username,
        'token': token
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
    user = auth.authenticate(request, username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return redirect("/index/")
    else:
        return redirect("/login?login_fail=1")


"""
Finaliza la sesión del usuario.
"""
def logoutView(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect("/index/")


"""
Formulario para registrar nuevo usuario.
"""
def signUpView(request):
    form = forms.SignUpForm()
    username_in_use = request.GET.get('username_in_use', 0)
    email_in_use = request.GET.get('email_in_use', 0)
    password_mismatch = request.GET.get('password_mismatch', 0)
    return render(request, 'signup.html', context={
        'form': form,
        'username_in_use': username_in_use,
        'email_in_use': email_in_use,
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
    if User.objects.filter(username=username).exists():
        return redirect("/sign-up?username_in_use=1")
    if User.objects.filter(email=email).exists():
        return redirect("/sign-up?email_in_use=1")
    if password != confirm_password:
        return redirect("/sign-up?password_mismatch=1")

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    user.save()
    token = models.UserTokens(user_id=user.id)
    token.save()

    return redirect("/index/")


"""
Redirige a la URL larga. Si no existe una URL asociada o esta es privada,
redirige a /index/.
"""
def redirectView(request, short_url):
    try:
        url = models.URLs.objects.get(short_url=short_url)
    except models.URLs.DoesNotExist:
        return redirect("/index/")

    if request.user.is_authenticated:
        user_id = request.user.id
    elif not url.is_private:
        user_id = None
    else:
        return redirect("/index/")

    if url.is_private and not models.URLAllowList.objects.filter(
        user_id=user_id,
        url_id=url.id
    ).exists():
        return redirect("/index/")

    visualization = models.URLVisualizations(
        user_id=user_id,
        url_id=url.id
    )
    visualization.save()
    return redirect(url.long_url)
