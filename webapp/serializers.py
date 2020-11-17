from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','email','last_login','is_superuser']

class StatusSerializer(serializers.Serializer):
    status=serializers.CharField(max_length=50)

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=ShippingAddress
        fields='__all__'

class PreviousOrderSerializer(serializers.Serializer):
    class Meta:
        model=OrderItem
        fields='__all__'

# class ShippingAddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=ShippingAddress
#         field='__all__'

class OrderSerializer(serializers.Serializer):
    class Meta:
        model:OrderItem
        fields='__all__'