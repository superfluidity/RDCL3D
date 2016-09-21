from lib.topoModelCtrl import ModelController
from django.http import HttpResponse

# Create your views here.
def get_model_specification(request, modelname):
    # modelname = request.GET.get('model')
    mctrl = ModelController('')
    print modelname
    response = mctrl.jsonmodel(modelname)
    # print response
    response =  HttpResponse(response, content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    return response