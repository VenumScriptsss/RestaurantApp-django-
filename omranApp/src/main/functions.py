import pandas as pd 
import numpy as np
from .models import *
import ast

def prods_quantity(x):
  
    context={}
    s=ast.literal_eval(x)
    for key,value in s.items():
      try:
         context[Products.objects.filter(id=int(key)).first().prodName]=value
      except:continue
    
    return context



def deleted_products(prods,flagged):
    deleted=[]
    for i in range (len(prods)):
       deleted.append(compared(prods[i],flagged[i]))
    df=pd.DataFrame({0: deleted}) 
    return df
  
def compared (x1,x2):
  l=[]
  for i in x2.keys():
    try:
      x1[i]
    except:
      l.append(i)
  return l.copy()