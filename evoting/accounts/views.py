from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import Formlogin 
# Create your views here.
def login(request):
    forms = Formlogin()
    if request.method == 'POST':
        username = request.POST('username')
        password = request.POST('password')

        user = authenticate(request, username=username, password=password)

        if user is not None :
            login(request, user)
            return redirect('accounts/login.html')
    return render(request, 'accounts/login.html' )