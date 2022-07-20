from operator import mod
from statistics import mode
from django.db import models
from distutils.command.upload import upload
from email.mime import image
from django.contrib.auth.models import User
from django.forms import IntegerField
from django.utils.text import slugify
from django.urls import reverse


# Create your models here.
class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    phone = models.CharField(max_length=10,default="")
    street= models.CharField(max_length=50,default="")
    city  = models.CharField(max_length=20,default="")
    pin_code=models.IntegerField(default=None)    
    def __str__(self):
        return self.name


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    image=models.ImageField(upload_to='pics',default=True)
    slug = models.SlugField(max_length=15 , blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category,self).save(*args, **kwargs)
    
    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse('products_by_category', kwargs={'slug': self.slug})

class QuantityVariant(models.Model):
    variant_name = models.CharField(max_length=15)
    
    def __str__(self):
        return self.variant_name




class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name=models.TextField()    
    image=models.ImageField(upload_to='pics')
    selling_price=models.IntegerField()
    discount_price=models.IntegerField()
    quantity=models.PositiveIntegerField(null=False,default=1)
    quantity_type = models.ForeignKey(QuantityVariant , blank=True, null=True , on_delete=models.PROTECT)
    slug = models.SlugField(max_length=15 , blank=True)
    stock=models.PositiveIntegerField(default=1)


    def __str__(self):
        return self.product_name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category)
        super(Product,self).save(*args, **kwargs)
    

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)
    p_id=models.IntegerField(default=0)

    def __str__(self):
      return str(self.id)
    
    def totalindividual_cost(self):
        return self.quantity * self.product.discount_price


STATUS_OPTIONS=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)


class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    update_date=models.DateTimeField(auto_now=True)
    total_price=models.IntegerField(null=False,default=1)
    status=models.CharField(max_length=30,choices=STATUS_OPTIONS,default='Pending')
    payment_mode=models.CharField(max_length=40,null=False,default="")
    payment_id=models.CharField(max_length=40,null=True,default="")
    tracking_number=models.CharField(max_length=100,null=True,default="")

    def __str__(self):
        return  "{} - {}".format(self.id,self.tracking_number)
   

    def filter_bytime(u_id):
        orders=OrderPlaced.objects.filter(user=u_id) 
        return orders

class OrderItems(models.Model):
    order=models.ForeignKey(OrderPlaced,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    price=models.IntegerField(null=False)
    quantity=models.IntegerField(null=False)

    def __str__(self):
        return "{} - {}".format(self.order.id,self.order.tracking_number)
   
