from django.shortcuts import render,redirect
from django.urls import reverse
from main.models import Command
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os 
from django.contrib.auth import authenticate, login
from django.conf import settings
from .models import *
from django.db import connection
from django.forms.models import model_to_dict
import pandas as pd 
from datetime import datetime, date, timedelta
from django.core import serializers
from django.contrib.auth import logout
from .functions import *
from django.contrib.auth.decorators import login_required
# Create your views here.
import ast

def my_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        try :
            request.session['userType'] 
            return view_func(request, *args, **kwargs)
        except:
            return redirect(reverse('loginPage'))
    return wrapper


def log_out(request):
    logout(request)
    return redirect('loginPage')

def loginPage(request):
    context = {}
    users = User.objects.all()
    
    if 'login' in request.POST:
       
        username = request.POST['username']
        pw = request.POST['password']
        for user in users:
            
            if username == user.username and pw == user.password:
                
                request.session['userType'] = user.userPriority
                return redirect('home')
            else:
                pass
    return render(request,"main/login.html",context)


def add_user(request):
    print("okey nigga")
    if request.method=="POST":
        user_name = request.POST.get('name')
        user_password = request.POST.get('password')
        user_type = request.POST.get('type')
        user_type=int(user_type)
        User(username=user_name,password=user_password,userPriority=user_type).save()
    all_user=pd.DataFrame(User.objects.all().values())
    context={"users":all_user['username']}
    return render(request, "main/add_user.html",context)
@csrf_exempt
def apply_function(request):
   
    if request.method == 'POST':
        id_= request.POST.get("id")
        comnd=Command.objects.get(id=id_)
        comnd.encaisser=True
        comnd.save()
    return render(request,"main/home.html")


def user_list_view(request):
    return render(request, "main/user_list.html")

#-------------ajouter/editer command----------------lzm tedkhel mn caissier wdir edit w ab3at lform bch tbanlk


def ajouterEditCommandView(request):
    context = {}
    context['prods'] = Products.objects.all()
    context['pageType'] = 'Ajouter Command'

    if 'edit' in request.POST:
        context['pageType'] = 'Editer Command'
        comm=Command.objects.get(id=request.POST['edit'])
        context['comm'] = comm
        commQnt = eval(comm.prods_quantity)
        
        context['commQnt'] = commQnt
       
    
    if 'confEdit' in request.POST:
        # if user chooses new command
        if request.POST['confEdit'] == 'newComm':
            # if request.POST.getlist('prodId_Qnt')
            comm = Command()
            comm.save()
            for prod in request.POST.getlist('prodId_Qnt'):
                id_qnt = prod.split(',')
                if id_qnt[1] == '0':
                    continue
                plat = Products.objects.get(id=id_qnt[0])
                comm.prods.add(plat)
                prodQnt = eval(comm.prods_quantity)
                prodQnt.update({int(id_qnt[0]):id_qnt[1]})
                comm.prods_quantity = str(prodQnt)
            comm.commPrice = request.POST['commPrix']
            
            if request.POST['typeComm'] == 'emporter':
                comm.commType = '1'
                comm.tableNum = '-1'
            else:                
                comm.commType = '2'
                comm.tableNum = request.POST['typeComm']
            comm.save()    
            return redirect('home')
        else:
            comm = Command.objects.get(id = request.POST['confEdit'])
            
            for prod in request.POST.getlist('prodId_Qnt'):
                id_qnt = prod.split(',')
                plat = Products.objects.get(id=id_qnt[0])
                comm.prods.add(plat)
                prodQnt = eval(comm.prods_quantity)
                if int(id_qnt[0]) in prodQnt:
                    if int(prodQnt[int(id_qnt[0])])> int(id_qnt[1]):
                        if request.session['userType'] != '1':
                            
                            comm.flaged = True
                            deletedProdNum =  int(prodQnt[int(id_qnt[0])]) - int(id_qnt[1])
                            flagedProds =eval(comm.flaged_prods)
                            flagedProds.update({int(id_qnt[0]):deletedProdNum})
                            comm.flaged_prods = str(flagedProds)

                prodQnt.update({int(id_qnt[0]):id_qnt[1]})
                
                if prodQnt[int(id_qnt[0])] == '0':
                    prodQnt.pop(int(id_qnt[0]))
                    
                    comm.prods.remove(Products.objects.get(id=int(id_qnt[0])))
                
                comm.prods_quantity = str(prodQnt)
            comm.commPrice = request.POST['commPrix']
            
            if request.POST['typeComm'] == 'emporter':
                comm.commType = '1'
                comm.tableNum = '-1'
            else:                
                comm.commType = '2'
                comm.tableNum = request.POST['typeComm']
            comm.save()    
            return redirect('home')
    if 'cat' in request.POST:
        
        if request.POST['cat'] == 'trad':
          context['prods'] = Products.objects.filter(prodCat = '1')
        elif request.POST['cat'] == 'ff':
          context['prods'] = Products.objects.filter(prodCat = '2')
        else:
          context['prods'] = Products.objects.filter(prodCat = '3')

        # context['prods'] = Products.objects.get(prodCat = request.POST['cat'])

    return render(request,"main/ajouter_commande2.html",context) #lazm nzid redirect ll prev page w hadi lzmha session bch na3raf type ta3 luser
    """ return render(request,"main/ajouterEditerComm.html",context) """



def ajouter_modifier_product(request):
    context = {}
    if 'ajouterPrd' in request.POST:
        product_name = request.POST.get('name')
        price = float(request.POST.get('price'))
        category = int(request.POST.get('category'))
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
        

        
        prod = Products.objects.get(id=request.POST.get('id'))
        prod.prodName=request.POST.get('name')
        prod.prodPrix=float(request.POST.get('price'))
        prod.prodCat=request.POST.get('category')
        prod.isActive=request.POST.get('active')=='on'
        prod.save()
      
        return redirect('editer-products')        

    return render(request, "main/ajouter_modifier_product.html",context)

def editProdsView(request):
    context = {}
    prods = Products.objects.all().order_by('prodName')
    
    context['products'] = prods
    context['catList'] = ['Traditionel', 'Modern', 'Autres'] 
    if 'act-dis' in request.POST:
        prod = Products.objects.get(id=request.POST['act-dis'])
        prod.isActive = not prod.isActive
        prod.save()
    return render(request,"main/products2.html",context)

def delete_product(request):

    context = {}
    
    if 'delete_prod' in request.POST:
        Products.objects.get(id=request.POST['delete_prod']).delete()
        return redirect('editer-products')
    prods = Products.objects.all()
    context['products'] = prods
    return render(request,"main/products2.html",context)




@csrf_exempt
def search_product_function(request):
    if request.method == 'POST':
        data= request.POST.get("data")
        all_prods=pd.DataFrame(Products.objects.all().values())
        result=Products.objects.filter(prodName__contains=data)
        result_list = []
        for product in result:
            product_dict = model_to_dict(product)
            product_dict['img'] = product.img.url if product.img else None
            result_list.append(product_dict)
    print(all_prods['id'])
    return JsonResponse({'data': result_list,"ids":list(all_prods['id'])})

@csrf_exempt
def update_category_list(request):
    if request.method == 'POST':
        data= request.POST.get("data")
        prods=Products.objects.filter(prodCat=data)
        
        result_list = []
        for product in prods:
            product_dict = model_to_dict(product)
            product_dict['img'] = product.img.url if product.img else None
            result_list.append(product_dict)
        context={"data":result_list}
        
        
        return JsonResponse(context)

#--------------------------home------------------------------
@my_login_required
def homeView(request):
    context={}
    commnds=Command.objects.all().values()
    df=pd.DataFrame(commnds)

    prods=pd.DataFrame(Products.objects.all().values())
    
    prod_price={}
    for i,j in zip(prods['prodName'],prods['prodPrix']):
        prod_price[i]=j

    #df['flaged'] = df['flaged'].replace({True: 'yes', False: 'no'})
    #df['encaisser'] = df['encaisser'].replace({True: 'yes', False: 'no'})
    #df['commType'] = df['commType'].replace({2: True, 1: False})
    #df["dateComm"] = df["dateComm"].dt.strftime("%d-%m-%Y")
    #df['prods_quantity']=df['prods_quantity'].apply(lambda x :ast.literal_eval(x))
    df['prods_quantity']=df['prods_quantity'].apply(lambda x :prods_quantity(x))
    context['commands']=df.to_dict("records")
    
    l=[]
    for i in df['id']:
            l.append(list(Command.objects.filter(id=i).first().prods.values_list('prodName', flat=True)))
            #l.append(list(Command.objects.filter(id=i).first().prods.all()))
    for i, d in enumerate(context['commands']):
                    subject = l[i]
                    d['prodNames'] = subject
    context['prod_price']=prod_price
    context['userType']=request.session['userType']
    
    return render(request,'main/home.html',context)


@csrf_exempt
def encaicement(request):
   
    if request.method == 'POST':
       
       id=request.POST.get('id')
       cmnd=Command.objects.filter(id=id).first()
       cmnd.encaisser=True
       cmnd.save()
    return JsonResponse({})
    
#----------------------------history--------------------------

def history(request):
    context={}
    commnds=Command.objects.all().values()
    df=pd.DataFrame(commnds)

    prods=pd.DataFrame(Products.objects.all().values())
    
    prod_price={}
    for i,j in zip(prods['prodName'],prods['prodPrix']):
        prod_price[i]=j

    df['flaged'] = df['flaged'].replace({True: 'yes', False: 'no'})
    df['encaisser'] = df['encaisser'].replace({True: 'yes', False: 'no'})
    df['commType'] = df['commType'].replace({2: True, 1: False})
    #df["dateComm"] = df["dateComm"].dt.strftime("%d-%m-%Y")
    #df['prods_quantity']=df['prods_quantity'].apply(lambda x :ast.literal_eval(x))
    df['prods_quantity']=df['prods_quantity'].apply(lambda x :prods_quantity(x))
    df['flaged_prods']=df['flaged_prods'].apply(lambda x :prods_quantity(x))
    df['deleted_prods']=deleted_products(df['prods_quantity'],df['flaged_prods'])
  
    context['commands']=df.to_dict("records")
    
    l=[]
    for i in df['id']:
            l.append(list(Command.objects.filter(id=i).first().prods.values_list('prodName', flat=True)))
            #l.append(list(Command.objects.filter(id=i).first().prods.all()))
    for i, d in enumerate(context['commands']):
                    subject = l[i]
                    d['prodNames'] = subject
    context['prod_price']=prod_price
   
    return render(request, "main\history.html",context=context) #---------    ----------#

@my_login_required
def history_submit(request):
    
        context={}
        commnds=Command.objects.all().values()
        prods=pd.DataFrame(Products.objects.all().values())
    
        prod_price={}
        for i,j in zip(prods['prodName'],prods['prodPrix']):
            prod_price[i]=j
       
        #-----------------------------------------------
        df=pd.DataFrame(commnds)
        ids=df['id']
        Encaisser=request.POST.get('Encaisser')
        Suppression=request.POST.get('Suppression')
        date_from=request.POST.get('date_from')
        date_to=request.POST.get('date-to')
        
        if(Encaisser!=""):
          Encaisser=Encaisser=='true'  
          df=df[ df['encaisser']==Encaisser ]
          
        if(Suppression!=""):
          Suppression=Suppression=='true' 
          df=df[df['flaged']==Suppression ]
          
        if(date_to!=""):
           df=df[df['encaissementTime']<=date_to+" 23:59:59"]
        if(date_from!=""):
           df=df[df['encaissementTime']>=date_from]
        df['flaged'] = df['flaged'].replace({True: 'yes', False: 'no'})
        df['encaisser'] = df['encaisser'].replace({True: 'yes', False: 'no'})
        df['commType'] = df['commType'].replace({2: True, 1: False})
        df["dateComm"] = df["dateComm"].dt.strftime("%d-%m-%Y")
        l=[]
        for i in df['id']:
            l.append(list(Command.objects.filter(id=i).first().prods.values_list('prodName', flat=True)))
        #----------------------------------------------   
       
        df['prods_quantity']=df['prods_quantity'].apply(lambda x :ast.literal_eval(x))
        context['commands']=df.to_dict("records")
        for i, d in enumerate(context['commands']):
                    subject = l[i]
                    d['prodNames'] = subject

        context['prod_price']=prod_price
        context['ids']=list(ids)
        
        return JsonResponse(context)

#--------------------------------------------------------

def test(request):
    return render(request, 'main\\test.html',context={})
