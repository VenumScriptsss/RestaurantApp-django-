from django.shortcuts import render
from main.models import Command
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os 
from django.conf import settings
from .models import *


# Create your views here.

def caissierAdminView(request):
    context = {}
    context['commands'] = Command.objects.all()
    return render(request,"main/caissierAdmin.html",context)

def caissierView(request):
    context = {}
    context['commands'] = Command.objects.all()
    return render(request,"main/caissier.html",context)

def serveurView(request):
    context = {}
    context['commands'] = Command.objects.all()
    return render(request, "main/serveur.html", context)

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


def ajouterEditCommandView(request):
    context = {}
    context['prods'] = Products.objects.all()
    context['pageType'] = 'Ajouter Command'
    
    if 'edit' in request.POST:
        context['pageType'] = 'Editer Command'
        comm=Command.objects.get(id=request.POST['edit']) 
        context['comm'] = comm
    if 'confEdit' in request.POST:
        comm = Command.objects.get(id = request.POST['confEdit'])
        for prod in request.POST:
            if ['confEdit','csrfmiddlewaretoken'] in request.POST:
                continue
            prod = Products.objects.get(id=prod)
            comm.prods.add(prod)
        comm.save()
    return render(request,"main/ajouterEditerComm.html",context)



def ajouter_modifier_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('name')
        price = float(request.POST.get('price'))
        category = request.POST.get('category')
        is_active = request.POST.get('active')
        image = request.FILES.get('image')
    
    
        if image:
            img_name = str(image.name)
            img_path = os.path.join(settings.MEDIA_ROOT, img_name)
            with open(img_path, 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)

 
        
        product = Products(prodName=product_name, prodPrix=price, prodCat=category, isActive=is_active == 'on', img=img_name)
        product.save()

    context={}
    return render(request, "main/ajouter_modifier_product.html",context)


     