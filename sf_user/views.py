from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect

# Create your views here.
def login_view(request):
    logout(request)
    extra_data = {}
    next = ""
    if request.GET:
        next = request.GET['next']
    error_message = ''
    if request.POST:
        print request.POST.get('username')
        print request.POST.get('password')
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        print "Auth Result: " + str(user) + " -> " + str(user)
        if user and user.is_active:
            if user.is_authenticated():
                login(request, user)
                if next == "":
                    return HttpResponseRedirect('/home')
                else:
                    return HttpResponseRedirect(next)
        else:
            error_message = 'Login failed!'
    return render(request, 'login.html', {'error_message':error_message} )