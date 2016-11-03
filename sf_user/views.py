from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from sf_user.models import CustomUser
from django.utils import timezone


# Create your views here.
def login_view(request):
    if hasattr(request.user, "is_guest_user"):
        CustomUser.objects.get(id=request.user.id).delete()
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


def guest_login(request):
    #user = CustomUser.objects.get(id=request.user.id)
    if hasattr(request.user, "is_guest_user"):
        CustomUser.objects.get(id=request.user.id).delete()
    logout(request)
    next = ""
    guest_user_name = "Guesto"+str(timezone.now())
    guest_user_email = guest_user_name+"@guest.it"
    guest_user = CustomUser.objects.create(username=guest_user_name, is_guest_user="True", email=guest_user_email)
    print guest_user.username
    #user = authenticate(username=guest_user.username, password="guest")
    #print user.is_active
    if guest_user and guest_user.is_active:
        if guest_user.is_authenticated():
            login(request, guest_user)
            if next == "":
                return HttpResponseRedirect('/home')
            else:
                return HttpResponseRedirect(next)

    return render(request, 'login.html', {'error_message': 'New Guest session failed.'})

def register_view(request):

    logout(request)
    extra_data = {}
    next = ""
    if request.GET:
        next = request.GET['next']
    error_message = ''
    if request.POST:
        print "new user"
    return render(request, 'register_user.html', {'error_message':error_message} )