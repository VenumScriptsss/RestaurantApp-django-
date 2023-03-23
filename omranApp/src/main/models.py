from django.db import models
from django import forms
from datetime import datetime

# models

class User(models.Model):
    userPriorityChoices = [
        ('1','caissier admin'),
        ('2','caissier'),
        ('3','serveur'),
    ]
    username = models.CharField(max_length=14,verbose_name="username",null=False)
    password = models.CharField(max_length=30,verbose_name="password", null=False)
    userPriority = models.CharField(max_length=1,choices=userPriorityChoices,null=False,verbose_name="usertype")

    def __str__(self):
        return self.username
    

#--------------------------------


class Products(models.Model):
    prodCatChoices = [
        ('1', 'Traditionelle'),
        ('2', 'Modern'),
        ('3', 'Boissant')
    ]
    prodName = models.CharField(max_length=30,null=False,help_text='entrer le nom de produit',verbose_name='nom de produit')
    prodPrix = models.IntegerField(null=False,help_text='prix de produit',verbose_name='prix de produit')
    prodCat = models.CharField(max_length=1,choices=prodCatChoices,null=False,help_text='choisit la categorie de ce produit',verbose_name='categorie de produit')
    isActive = models.BooleanField(help_text='activer ou desactiver ce produit', verbose_name='status de produit',default=True)
    img=models.ImageField(default='default.jpg',upload_to='profile_pics')

    
    def __str__(self):
        return self.prodName
    

#-------------------


class Command(models.Model):
    commtypeChoices = [('1','emporter'),('2','a table')]
    commType = models.CharField(max_length=1,help_text='choisit le type de la command',choices=commtypeChoices,verbose_name='type de command')
    tableNum = models.IntegerField(null=False,help_text='enter le numero de la table',verbose_name='numero de table')
    prods = models.ManyToManyField(Products)
    dateComm = models.DateTimeField(auto_now_add=True,verbose_name='temps creation de la command')
    prods_quantity=models.CharField(max_length=750,default="{}")
    encaisser = models.BooleanField(verbose_name='status d encaissemnt',default=False)
    encaissementTime = models.DateTimeField(auto_now_add=True,verbose_name='temps encaissement')
    flaged = models.BooleanField(verbose_name='modification au command')
    commPrice = models.IntegerField(verbose_name='prix total command',default=0,null=False)

    def __str__(self):
        return str(self.id)