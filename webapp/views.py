from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib.sessions.models import Session
from django.utils import timezone
from rest_framework.response import Response
import urllib.request
import urllib.parse
import datetime
from .serializers import *

# Create your views here.
@csrf_exempt
def Userlogin(request):
    if request.method=='POST':
        username=request.POST.get("phone")
        # password=request.POST.get("password")

        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            user=None

        if user is not None:
            login(request,user)
            serializer = UserSerializer(user)
            return JsonResponse(serializer.data)
        else:
            data = {'status': 'User Not Found'}
            serializer = StatusSerializer(data=data)
            serializer.is_valid()
            return JsonResponse(serializer.data)

@csrf_exempt
def Userlogout(request):
    if request.method=='GET':
        logout(request)
        data={'status':'logged out successfully'}
        serializer=StatusSerializer(data=data)
        serializer.is_valid()
        return JsonResponse(serializer.data)

@csrf_exempt
def Userregister(request):
    if request.method=='POST':
        try:
            user=User.objects.get(username=request.POST.get("phone"))
        except User.DoesNotExist:
            user=None

        if user is None:
            user=User()
            user.username=request.POST.get("phone")
            user.email=request.POST.get("email")
            user.first_name=request.POST.get("first_name")
            user.save()

            serializer = UserSerializer(user)
            # serializer.is_valid()
            return JsonResponse(serializer.data)

        else:
            data = {'status': 'User already exist'}
            serializer=StatusSerializer(data=data)
            serializer.is_valid()
            return JsonResponse(serializer.data)

#store
@csrf_exempt
def products(request):
    if request.method == "GET":
        # category=Category.objects.filter(pk=pk)
        products=Product.objects.all()
        serializer=ProductsSerializer(products,many=True)
        # serializer.is_valid()
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def category(request,pk):
    if request.method == "GET":
        category = Category.objects.get(id = pk)
        print(category)
        products = Product.objects.filter(category=category)

        serializer = ProductsSerializer(products, many = True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def categories(request):
    if request.method == "GET":
        category = Category.objects.all()

        serializer = CategorySerializer(category, many = True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def cart(request):
    if request.user.is_authenticated:
        user=request.user
        order,created=Order.objects.get_or_create(user=user,complete=False)
        # query child objects by setting parents value
        # it will get all orderitems having order as parents
        items=order.orderitem_set.all()
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_item':0}
    context={'items':items,'order':order}
    return render(request)

@csrf_exempt
def checkout(request):
    if request.user.is_authenticated:
        username=request.user.username
        order,created=Order.objects.get_or_create(username=username,complete=False)
        # query child objects by setting parents value
        # it will get all orderitems having order as parents
        items=order.orderitem_set.all()
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_item':0}

    context={'items':items,'order':order}
    return render(request)

@csrf_exempt
def getshipping_details(request):
    if request.method=='GET':
        user=request.user
        address=ShippingAddress.objects.filter(user=user)
        serializer = RegisterSerializer(address,many=True)
        return JsonResponse(serializer.data,safe=False)


@csrf_exempt
def addshipping_details(request):
    if request.method=='POST':
        user=request.user.is_authenticated
        print(user)
        if user is not False:
            # order = Order.objects.get(customer=customer)
            #if order.complete == True:

            ads = ShippingAddress()
            user_id=request.POST.get("user_id")
            user = User.objects.get(id=user_id)
            ads.user = user
            ads.address = request.POST.get("address")
            ads.city = request.POST.get("city")
            ads.state = request.POST.get("state")
            ads.zip_code = request.POST.get("zip_code")
            ads.phone_no = request.POST.get("phone_no")
            ads.save()
            serializer = RegisterSerializer(ads)
            return JsonResponse(serializer.data)

@csrf_exempt
def PreviousOrder(request):
    if request=='GET':
        user=request.user
        order=OrderItem.objects.all(user=user)
        serializer = PreviousOrderSerializer(order,many=True)
        return JsonResponse(serializer.data)


@csrf_exempt
def sendotp(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        otp = request.POST.get("otp")

        apikey = "Qx2Iq5DK8og-mPmM3Y66TAMGDsIRqsxsYtcJuq7SK8"
        message = "Your one time password to log into app is " + otp

        data =  urllib.parse.urlencode({
            'apikey': apikey,
            'numbers': phone,
            'message' : message
            })

        data = data.encode('utf-8')
        request = urllib.request.Request("https://api.textlocal.in/send/?")
        f = urllib.request.urlopen(request, data)
        fr = f.read()
        return JsonResponse({"status":"success"})

def createorder(request):
    if request.method=='POST':
        items= request.POST.get("items")
        order =Order()
        order.user = request.user
        order.date_ordered = datetime.date.today()
        order.complete = False
        sh_id = request.POST.get("shipping_address_id")
        shipping_add = ShippingAddress.objects.get(id = sh_id)
        order.shipping_address = shipping_add

        total_price = 0

        for item in items:
            p_item =OrderItem()
            p_item.order = order
            product = Product.objects.get(id=item.product.product_id)
            p_item.product = product
            p_item.quantity = item.quantity
            total_price = total_price + product.product_price * item.quantity
        p_item.total=total_price
        serializer = OrderSerializer(p_item, many=True)
        return JsonResponse(serializer.data, safe=False)
