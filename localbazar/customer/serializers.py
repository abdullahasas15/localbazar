from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Customer, Order, Product, Shop, Category

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image']

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = [
            'id', 'name', 'description', 'location', 'phone', 
            'email', 'image', 'is_active', 'created_at', 'updated_at'
        ]

class ProductSerializer(serializers.ModelSerializer):
    shop = ShopSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'image', 
            'category', 'shop', 'stock_quantity', 'is_active', 
            'created_at', 'updated_at'
        ]

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone', 'address', 'date_joined', 'is_active'
        ]
        read_only_fields = ['id', 'date_joined']

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Customer
        fields = [
            'username', 'email', 'password', 'confirm_password',
            'first_name', 'last_name', 'phone', 'address'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = Customer.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class OrderItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'items', 'total_amount', 'status',
            'shipping_address', 'payment_method', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'customer', 'total_amount', 'created_at', 'updated_at']

class CartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class CartSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

class SearchSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=255, required=False)
    category = serializers.CharField(max_length=100, required=False)
    location = serializers.CharField(max_length=255, required=False)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    sort_by = serializers.ChoiceField(
        choices=['name', 'price', 'created_at', 'rating'],
        required=False
    )
    sort_order = serializers.ChoiceField(
        choices=['asc', 'desc'],
        required=False
    ) 