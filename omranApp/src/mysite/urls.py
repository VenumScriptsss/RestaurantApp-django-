"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
#from main.views import caissierAdminView,caissierView,loginPage,apply_function
from main.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('caissierAdmin', caissierAdminView, name='caissierAdmin'),
    path('caissier', caissierView, name='caissier'),
    path('serveur', serveurView, name='serveur'),
    path('', loginPage, name='loginPage'),
    path('apply_function', apply_function, name='apply_function'),
    path('ajouter-command', ajouterEditCommandView, name='ajouter-command'),
    path('editer-command', ajouterEditCommandView, name='editer-command'),
    path('ajouterEditer-product', ajouter_modifier_product, name='ajouterEditer-product'),
    path('editer-products', editProdsView, name='editer-products'),
    path('delete_product', delete_product, name='delete_product'),
    path('search_product_function', search_product_function, name='search_product_function'),
    path('home', homeView, name='home'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
