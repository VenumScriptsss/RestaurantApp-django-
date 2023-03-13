from django.shortcuts import render,redirect
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
    users = User.objects.all()
    if 'login' in request.POST:
        username = request.POST['uname']
        pw = request.POST['psw']
        for user in users:
            if username == user.username and pw == user.password:
                print("found user")
                if user.userPriority == '1':
                    return redirect('caissierAdmin')
                elif user.userPriority == '2':
                    return redirect('caissier')
                elif user.userPriority == '3':
                    return redirect('serveur')
    return render(request,"main/loginPage.html")


@csrf_exempt
def apply_function(request):
   
    if request.method == 'POST':
        id_= request.POST.get("id")
        comnd=Command.objects.get(id=id_)
        comnd.encaisser=True
        comnd.save()
    return render(request,"main/caissierAdmin.html")


#-------------ajouter/editer command----------------lzm tedkhel mn caissier wdir edit w ab3at lform bch tbanlk


def ajouterEditCommandView(request):
    context = {}
    context['prods'] = Products.objects.all()
    context['pageType'] = 'Ajouter Command'
    
    if 'edit' in request.POST:
        context['pageType'] = 'Editer Command'
        comm=Command.objects.get(id=request.POST['edit']) 
        context['comm'] = comm
    print(request.POST)
    if 'confEdit' in request.POST:
        comm = Command.objects.get(id = request.POST['confEdit'])
        for prod in request.POST:
            if prod in ['confEdit','csrfmiddlewaretoken']:
                print("skippedd ",request.POST)
                continue
            prod = Products.objects.get(id=request.POST[prod])
            comm.prods.add(prod)
            comm.commPrice+= prod.prodPrix
        comm.save()
    return render(request,"main/ajouterEditerComm.html",context)



def ajouter_modifier_product(request):
    context = {}
    if 'ajouterPrd' in request.POST:
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
    
        return redirect('editer-products')
    
    if 'editPrd' in request.POST:
        prod = Products.objects.get(id=request.POST['editPrd'])
        context['editing'] = True
        context['prod'] = prod

    if 'confirmEdit' in request.POST:
            
        prod.prodName=request.POST['name']
        prod.prodPrix=request.POST['price']
        prod.prodCat=request.POST['category']
        prod.isActive=request.POST['active']
        prod.img=request.POST['img']
        prod.save()
        return redirect('caissierAdmin')        

    return render(request, "main/ajouter_modifier_product.html",context)

def editProdsView(request):
    context = {}
    prods = Products.objects.all()
    context['products'] = prods
    if 'act-dis' in request.POST:
        prod = Products.objects.get(id=request.POST['act-dis'])
        prod.isActive = not prod.isActive
        prod.save()
    return render(request,"main/products.html",context)
     