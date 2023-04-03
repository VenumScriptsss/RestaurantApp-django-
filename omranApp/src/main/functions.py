import pandas as pd 
import numpy as np
from .models import *
import ast

def prods_quantity(x):
    print(ast.literal_eval(x))
    context={}
    s=ast.literal_eval(x)
    for key,value in s.items():
      try:
         context[Products.objects.filter(id=int(key)).first().prodName]=value
      except:continue
    
    return context

     

