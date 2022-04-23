from unicodedata import name
from django.shortcuts import render, redirect,HttpResponseRedirect
from cinetpay_sdk.s_d_k import Cinetpay

from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
import random

from store.models.product import Products
from store.models.orders import Order



class CheckOut(View):
    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        address=request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        country = request.POST.get('country')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Products.get_products_by_id(list(cart.keys()))
        prix=0
        x = random.randint(0,10000000000)
        for product in products:
            prix=product.price+prix
        print(prix)
        apikey = "20816034206262c82a727fe0.78787435"
        site_id = "640649"
        client = Cinetpay(apikey,site_id)
        data = { 
            'amount' : 100,
            'currency' : "XOF",            
            'transaction_id' : x,  
            'description' : "TRANSACTION DESCRIPTION",  
            'return_url' : "https://www.google.com/",
            'notify_url' : "https://www.google.com/",  
            'customer_name' :name,                     
            'customer_surname' : email   
        }
        x=client.PaymentInitialization(data)
        y=x['data']
        z=y['payment_url']
        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}

        return HttpResponseRedirect('{}'.format(z))
