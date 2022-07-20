from hashlib import new
import imp
from itertools import product
from math import prod
from multiprocessing import context
from random import random
from turtle import home
from unicodedata import name
from urllib import request
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Q
from django.http.response import HttpResponseRedirect
import random

# Create your views here.
class HomeView(View):
     def get(self,request):
        categories =Category.objects.all()
        products   =Product.objects.all()
        data={
                'products':products,
                'categories':categories

            }
        return render(request,'base.html',data)


class products_by_category(View):
     def get(self,request,slug):
          category=slug
          print(category)
          if category=="all":
               products=Product.objects.all()
               return render(request,'category_wise.html',{'products':products})
          else:
               products=Product.objects.filter(slug__icontains=category)
               return render(request,'category_wise.html',{'products':products})
            

class search_bar(View):
     def get(self,request):
          query=request.GET.get('query')
          print(query)
          if query:
               products=Product.objects.filter(product_name__icontains=query)
               return render(request,'searchbar.html',{'products':products})
          else:
               return render(request,'searchbar.html',{})

class RegistrationView(View):
     def get(self,request):
          form= CustomerRegistration()
          return render(request,'RegistrationPage.html',{'form':form})
     def post(self,request):
          form=CustomerRegistration(request.POST)
          if form.is_valid():
               messages.success(request,'Yeah! You have successfully registered.')
               form.save()
          return render(request,'RegistrationPage.html',{'form':form})
   
class ProfileView(View):
     def get(self,request):
          form=MyProfileForm
          return render(request,'profile.html',{'form':form,'active':'btn-primary'})
     
     def post(self,request):
          form=MyProfileForm(request.POST)
          if form.is_valid():
               user=request.user
               name=form.cleaned_data['name']
               locality=form.cleaned_data['street']
               mob_no=form.cleaned_data['phone']
               city=form.cleaned_data['city']
               pin=form.cleaned_data['pin_code']
               pro=Customer(user=user,name=name,street=locality,phone=mob_no,city=city,pin_code=pin)
               pro.save()
               messages.success(request,'Profile is updated successfully.')
          return render(request,'profile.html',{'form':form,'active':'btn-primary'})
               

          

class AddresView(View):
     def get(self,request):
          adds=Customer.objects.filter(user=request.user)
          return render(request,'address.html',{'add':adds,'active':'btn-primary'})


class Add_to_cart(View):
     def get(self,request):
          user=request.user
          pid=request.GET.get('product_id')
          prod=Product.objects.get(id=pid)
          p=Cart.objects.filter(p_id=pid,user=user)
          if p:
               print('present')
               messages.warning(request,'Item is already present in your cart.')
               return redirect('/')
          else:
               print(prod.id)   
               Cart(user=user,product=prod,p_id=pid).save()
               messages.warning(request,'Item successfully added to your cart.')
          return redirect('/')

class Show_cart(View):
     def get(self,request):
          if request.user.is_authenticated:
               user=request.user
               # cart_products=Cart.objects.filter(user=user)
               products=[p for p in Cart.objects.all() if p.user==user]
               
               mrp=0
               shipping=0
               if products:    
                    for p in products:  
                        
                         
                         tamt=(p.quantity*p.product.discount_price)
                         mrp+=tamt
               
                    return render(request,'cart.html',{'products':products,'mrp':mrp
                              ,'tprice':mrp+shipping})
                        
                   
               else:
                    return render(request,'cart.html')


class Increase_Quantity(View):
     def get(self,request):
          pid=request.GET['p_id']
          # print(pid)
          c=Cart.objects.get(Q(product=pid) & Q(user=request.user))
          
          mrp=0
          shipping=0
          # if(c.quantity<=c.product.stock):
          c.quantity+=1
          # Product.quantity+1
          Product.quantity=c.quantity
          # print(Product.quantity)
          c.save()
     # else:
          data={
               'quantity':c.quantity,
               'amount':mrp,
               'totalamount':mrp+shipping,
          #   'status':'only',
               
          }
          products=[p for p in Cart.objects.all() if p.user==request.user]
          for p in products:
               tamt=(p.quantity * p.product.discount_price)
               mrp+=tamt
              
          data={
                 'quantity':c.quantity,
                 'amount':mrp,
                 'totalamount':mrp+shipping,
                 
          }
          return JsonResponse(data)

class Decrease_Quantity(View):
     def get(self,request):
          p_id=request.GET['pid']
          print(p_id)
          c=Cart.objects.get(Q(product=p_id) & Q(user=request.user))
          c.quantity-=1
          if c.quantity>0:
               Product.quantity=c.quantity
               c.save()
          else:
               c.delete()
          products=[p for p in Cart.objects.all() if p.user==request.user]
          mrp=0
          shipping=0
          for p in products:
               tamt=(p.quantity * p.product.discount_price)
               mrp+=tamt
               
          data={
                 'quantity':c.quantity,
                 'amount':mrp,
                 'totalamount':mrp+shipping,
                 
          }
          return JsonResponse(data)

class Remove_Product(View):
     def get(self,request):
          p_id=request.GET['pid']
          c=Cart.objects.get(Q(product=p_id) & Q(user=request.user))
          c.delete()
          products=[p for p in Cart.objects.all() if p.user==request.user]
          mrp=0
          shipping=0
          for p in products:
               tamt=(p.quantity * p.product.discount_price)
               mrp+=tamt
          
          data={
                 'amount':mrp,
                 'totalamount':mrp+shipping,
                 
          }
          return JsonResponse(data)


class Checkout(View):
     def get(self,request):
          user=request.user
          address=Customer.objects.filter(user=user)
          cart_items=Cart.objects.filter(user=user)
          cart_products=[p for p in Cart.objects.all() if p.user==request.user]
          mrp=0
          shipping=0
          if cart_products:
               for p in cart_products:
                    tamt=(p.quantity * p.product.discount_price)
                    mrp+=tamt
               totalamount=mrp+shipping
               return render(request,'checkout.html',{'add':address,'tamt':totalamount,'items':cart_items})

class PlaceOrder(View):
     def post(self,request):
          user=request.user
          neworder=OrderPlaced()
          cidd=request.POST.get('custadd')
          print("111")
          print(cidd)
          customer=Customer.objects.get(id=cidd)
          neworder.customer=customer
          neworder.user=user
          neworder.payment_mode=request.POST.get('payment_mode')
          neworder.payment_id=request.POST.get('payment_id')
          cart=Cart.objects.filter(user=user)
          cart=[p for p in Cart.objects.all() if p.user==request.user]
          tp=0
          i=0
          for p in cart:     
               tp=tp+  p.quantity * p.product.discount_price 
               i=i+1
          neworder.total_price=tp
          neworder.quantity=i
          track_no=str(customer)  + str(random.randint(1111111,9999999))

          while OrderPlaced.objects.filter(tracking_number=track_no) is None:
               track_no=str(customer) + str(random.randint(1111111,9999999))
          
          neworder.tracking_number=track_no
          neworder.save()

          neworderitems=Cart.objects.filter(user=user)
          for i in neworderitems:
               OrderItems.objects.create(
                    order=neworder,
                    product=i.product,
                    price=i.product.discount_price,
                    quantity=i.quantity
               )
          
          Cart.objects.filter(user=user).delete()
          

          paymode=request.POST.get('payment_mode')

          if paymode=="Paid Online":
               return JsonResponse({'status':"Your order has been placed successfully."})
          else:
              messages.success(request,"Your order has been placed successfully.")
              return redirect('/')


# class Payment(View):
#      def post(self,request):
#           user=request.user
#           cid=request.POST.get('custadd')
#           print(cid)
#           cust=Customer.objects.get(id=cid)
#           cart=Cart.objects.filter(user=user)
#           for c in cart:
#                OrderPlaced(user=user,customer=cust,product=c.product,quantity=c.quantity).save()
#                c.delete()
#           return redirect("cart")

class My_Orders(View):
     def get(self,request):
          user=request.user
          print(user.id)
          orders=OrderPlaced.objects.filter(user=request.user)
          # all_items=OrderPlaced.objects.filter(user=request.user,customer=)
          return render(request,'my_orders.html',{'orders':orders})


class Razorpay(View):
     def get(self,request):
         user=request.user
     #     cid=request.GET['cid']
         print("hii")
     #     print(cid)
         cart=Cart.objects.filter(user=user)
         cart_items=[p for p in Cart.objects.all() if p.user==request.user]
         tp=0
         for p in cart_items:     
               tp=tp+  p.quantity * p.product.discount_price 

         return JsonResponse({
              'total_price':tp,
          #     'cust_add':cid

         })
 
         
class Detail_view(View):
     def get(self,request,t_no):
          order=OrderPlaced.objects.filter(tracking_number=t_no).filter(user=request.user).first()
          order_items=OrderItems.objects.filter(order=order)
          return render(request,'detailview.html',{'order':order,'orderitems':order_items})