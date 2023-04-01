import pandas as pd 
import numpy as np
from .models import *
def prods_quantity(x):
    Products.objects.filter(id=1).prodName
    context={}
    s=ast.literal_eval(x)
    for key,value in x.items():
      try:
         context[Products.objects.filter(id=int(key)).first().prodName]=value
      except:continue
    
    return context

     

