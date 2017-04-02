from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from projecthandler.models import Project
from deploymenthandler.models import Deployment
from sf_user.models import CustomUser


@login_required
def home(request):
    user = CustomUser.objects.get(id=request.user.id)
    projects = Project.objects.filter(owner=user).select_subclasses()
    #projects = []
    print request.user.has_perm('deploymenthandler')
    deployments = Deployment.objects.filter(creator_id=request.user.id)
    result = {
        'projects': len(projects) if projects else 0,
        'deployments': len(deployments) if deployments else 0,
    }
    return render(request, 'home.html', result)


def forbidden(request):
    return render(request, 'forbidden.html')



