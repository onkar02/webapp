from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    category_name=models.CharField(max_length=50,default="")

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_id=models.AutoField
    # category_name=models.ForeignKey(Category,default="",on_delete=models.CASCADE,null=True,blank=True)
    product_name=models.CharField(max_length=100)
    product_price=models.FloatField()
    product_discription=models.TextField(default="")
    pub_date=models.DateField()
    product_image=models.ImageField(null=True,blank=True,default="")
    product_in_stock=models.IntegerField()
    category = models.ForeignKey(Category,default="",on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


    @property
    def imageURL(self):
        try:
            url=self.product_image.url
        except:
            url=''
        return url

class ShippingAddress(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    state = models.CharField(max_length=20,default="")
    city = models.CharField(max_length=20,default="")
    zip_code = models.CharField(max_length=10,default="")
    address = models.CharField(max_length=100, default="")
    phone_no=models.CharField(max_length=20,default="")
    date_added=models.DateTimeField(auto_now_add=True)



# whole order
class Order(models.Model) :
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    # if the order taken from user is complete or not
    complete=models.BooleanField(default=False)
    # transaction_id=models.CharField(max_length=50,default=" ")
    shipping_address = models.OneToOneField(ShippingAddress,default="",on_delete=models.CASCADE)

    def __str__(self):
        return str(self.transaction_id)

    # @property
    # def get_cart_total(self):
    #     orderitems=self.orderitem_set.all()
    #     total=sum([item.get_total for item in orderitems])
    #     return total
    #
    # @property
    # def get_cart_items(self):
    #     orderitems=self.orderitem_set.all()
    #     total=sum([item.quantity for item in orderitems])
    #     return total

# single item of order (child of Order)
class OrderItem(models.Model) :
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    total=models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    # @property
    # def get_total(self):
    #     total=self.product.product_price*self.quantity
    #     return total

    def __str__(self):
        return self.address

