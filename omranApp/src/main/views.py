from django.shortcuts import render,redirect
from main.models import Command
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os 
from django.conf import settings
from .models import *

from django.forms.models import model_to_dict
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
    users = User.objects.all()
    print(request.POST)
    if 'login' in request.POST:
        print("yoo")
        username = request.POST['username']
        pw = request.POST['password']
        for user in users:
            if username == user.username and pw == user.password:
                print("found user")
                request.sessoin['userType'] = user.userPriority

    return render(request,"main/login.html",context)


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
    if 'confEdit' in request.POST:
        if not request.POST['confEdit'] == 'newComm':
            comm = Command.objects.get(id = request.POST['confEdit'])
            print(request.POST)
            for prod in request.POST:
                if prod in ['csrfmiddlewaretoken','confEdit','number']:
                    continue
                prod = Products.objects.get(id=request.POST[prod])
                comm.prods.add(prod)
                comm.commPrice+= prod.prodPrix
            comm.save()
    if 'cat' in request.POST:
        print(request.POST['cat'])
        if request.POST['cat'] == 'trad':
          context['prods'] = Products.objects.filter(prodCat = '1')
        elif request.POST['cat'] == 'ff':
          context['prods'] = Products.objects.filter(prodCat = '2')
        else:
          context['prods'] = Products.objects.filter(prodCat = '3')

        # context['prods'] = Products.objects.get(prodCat = request.POST['cat'])

    return render(request,"main/page-1.html",context) #lazm nzid redirect ll prev page w hadi lzmha session bch na3raf type ta3 luser
    """ return render(request,"main/ajouterEditerComm.html",context) """



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
        print(request.POST)

        
        prod = Products.objects.get(id=request.POST.get('id'))
        prod.prodName=request.POST.get('name')
        prod.prodPrix=float(request.POST.get('price'))
        prod.prodCat=request.POST.get('category')
        prod.isActive=request.POST.get('active')=='on'
        prod.save()
      
        return redirect('caissierAdmin')        

    return render(request, "main/ajouter_modifier_product.html",context)

def editProdsView(request):
    context = {}
    prods = Products.objects.all().order_by('prodName')
    
    context['products'] = prods
    if 'act-dis' in request.POST:
        prod = Products.objects.get(id=request.POST['act-dis'])
        prod.isActive = not prod.isActive
        prod.save()
    return render(request,"main/products.html",context)

def delete_product(request):

    context = {}
    
    if 'delete_prod' in request.POST:
        print('done')
        Products.objects.get(id=request.POST['delete_prod']).delete()
    prods = Products.objects.all()
    context['products'] = prods
    return render(request,"main/products.html",context)


@csrf_exempt
def search_product_function(request):
    if request.method == 'POST':
        data= request.POST.get("data")
        result=Products.objects.filter(prodName__contains=data)
        result_list = []
        for product in result:
            product_dict = model_to_dict(product)
            product_dict['img'] = product.img.url if product.img else None
            result_list.append(product_dict)
        print(result_list)
    return JsonResponse({'data': result_list })

def homeView(request):
    context = {}
    
