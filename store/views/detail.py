from django.shortcuts import render , redirect , HttpResponseRedirect,get_list_or_404
from store.models.product import Products

def details(request,id):
    product=get_list_or_404(Products,id=id)
    return render(request,'index1.html',{"product":product})
