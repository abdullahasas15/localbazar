from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.db.models import Q
from .models import Customer, Order, Product, Shop
from .serializers import (
    CustomerSerializer, OrderSerializer, ProductSerializer, 
    ShopSerializer, CustomerRegistrationSerializer
)

# Customer Views
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

class CustomerRegistrationView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class CustomerLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                serializer = CustomerSerializer(user)
                return Response({
                    'user': serializer.data,
                    'message': 'Login successful'
                })
            else:
                return Response({
                    'error': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'error': 'Email and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)

class CustomerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

# Order Views
class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)

class OrderCancelView(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)
    
    def update(self, request, *args, **kwargs):
        order = self.get_object()
        if order.status in ['pending', 'confirmed']:
            order.status = 'cancelled'
            order.save()
            return Response({'message': 'Order cancelled successfully'})
        return Response({'error': 'Order cannot be cancelled'}, status=status.HTTP_400_BAD_REQUEST)

# Product Views
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        category = self.request.query_params.get('category', None)
        search = self.request.query_params.get('search', None)
        
        if category:
            queryset = queryset.filter(category__name__icontains=category)
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search) |
                Q(shop__name__icontains=search)
            )
        
        return queryset

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class ProductSearchView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if query:
            return Product.objects.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(shop__name__icontains=query),
                is_active=True
            )
        return Product.objects.none()

class ProductCategoryView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        category = self.kwargs.get('category')
        return Product.objects.filter(
            category__name__icontains=category,
            is_active=True
        )

# Shop Views
class ShopListView(generics.ListAPIView):
    queryset = Shop.objects.filter(is_active=True)
    serializer_class = ShopSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Shop.objects.filter(is_active=True)
        location = self.request.query_params.get('location', None)
        
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        return queryset

class ShopDetailView(generics.RetrieveAPIView):
    queryset = Shop.objects.filter(is_active=True)
    serializer_class = ShopSerializer
    permission_classes = [permissions.AllowAny]

class ShopProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        shop_id = self.kwargs.get('pk')
        return Product.objects.filter(shop_id=shop_id, is_active=True)

# Cart Views (Simplified - you might want to use sessions or a separate cart model)
class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # This is a simplified cart implementation
        # In a real app, you'd have a Cart model
        return Response({'message': 'Cart functionality to be implemented'})
    
    def post(self, request):
        return Response({'message': 'Cart functionality to be implemented'})

class CartAddItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        return Response({'message': 'Add to cart functionality to be implemented'})

class CartRemoveItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, pk):
        return Response({'message': 'Remove from cart functionality to be implemented'})

class CartUpdateItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self, request, pk):
        return Response({'message': 'Update cart functionality to be implemented'})

class CartClearView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request):
        return Response({'message': 'Clear cart functionality to be implemented'})

# API Health Check
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_health_check(request):
    return Response({
        'status': 'healthy',
        'message': 'LocalBazar API is running',
        'version': '1.0.0'
    })
