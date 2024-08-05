from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def system_login(request):
    """
    View for system login. If the user request is a GET, it will render the login page.
    Otherwise, the view will try to authenticate the user and redirect to the dashboard if successful.
    """
    if request.user.is_authenticated:
        return redirect('/')

    context = {"error": None}
    # If the request is a POST, it will try to authenticate the user.
    # Else, it will render the login page with an error message.
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)

            # add a token cookie
            response = redirect('/')
            response.set_cookie('token', user.auth_token.key)

            return response
        context['error'] = "Usuário e senha inválidos!"

    return render(request, 'login.html', context)


def system_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/login')


@login_required
def dashboard(request):
    context = {
        'user': request.user
    }
    return render(request, "dashboard.html", context)
