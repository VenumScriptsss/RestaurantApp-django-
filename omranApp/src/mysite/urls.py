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

    path('', loginPage, name='loginPage'),
    path('apply_function', apply_function, name='apply_function'),
    path('ajouter-command', ajouterEditCommandView, name='ajouter-command'),
    path('editer-command', ajouterEditCommandView, name='editer-command'),
    path('ajouterEditer-product', ajouter_modifier_product, name='ajouterEditer-product'),
    path('editer-products', editProdsView, name='editer-products'),
    path('delete_product', delete_product, name='delete_product'),
    path('search_product_function', search_product_function, name='search_product_function'),
    path('home', homeView, name='home'),
    path('products2', editProdsView, name='product'),
    path('history', history, name='history'),
    path('history_submit', history_submit, name='history_submit'),
    path('update_category_list', update_category_list, name='update_category_list'),
    path('logout', log_out, name='logout'),
    path('encaicement', encaicement, name='encaicement'),
    path('cancelComm', cancelComm, name='cancelComm'),
    path('test', test, name='test'),
    path('add_user', add_user, name='add_user'),
     path('user_list', user_list_view, name='user_list'),
    path('edit_user', edit_user, name='edit_user'),
    path('edit_user_submit', edit_user_submit, name='edit_user_submit'),
    path('delete_user', delete_user, name='delete_user'),
    


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
