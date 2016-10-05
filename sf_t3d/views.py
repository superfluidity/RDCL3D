from django.shortcuts import render



def home(request, configuration_id=None):

    return render(request, 'home.html', {})





