from django.shortcuts import render
from main.models import Command
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Create your views here.

def caissierAdminView(request):
    context = {}
    context['commands'] = Command.objects.all()
    return render(request,"main/caissierAdmin.html",context)

def caissierView(request):
    context = {}
    context['commands'] = Command.objects.all()
    return render(request,"main/caissier.html",context)

def loginPage(request):
    context = {}
    context['commands'] = Command.objects.all()
    return render(request,"main/loginPage.html",context)


@csrf_exempt
def apply_function(request):
   
    if request.method == 'POST':
        id_= request.POST.get("id")
        comnd=Command.objects.get(id=id_)
        comnd.encaisser=True
        comnd.save()
    return render(request,"main/caissierAdmin.html")


#-------------ajouter/editer command----------------


def ajouterEeditCommandView(request):
    context = {}
    if 'ajouterCommand' in request.POST:
        context['pageType'] = 'Ajouter-Command'
    return render(request,"main/ajouterEditerComm.html",context)
