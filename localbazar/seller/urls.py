from django.urls import path
from . import views

app_name = 'seller'

urlpatterns = [
    # Seller API endpoints
    path('sellers/', views.SellerListCreateView.as_view(), name='seller-list-create'),
    path('sellers/<int:pk>/', views.SellerDetailView.as_view(), name='seller-detail'),
    path('sellers/register/', views.SellerRegistrationView.as_view(), name='seller-register'),
    path('sellers/login/', views.SellerLoginView.as_view(), name='seller-login'),
    path('sellers/profile/', views.SellerProfileView.as_view(), name='seller-profile'),
    
    # Shop management endpoints
    path('shops/', views.ShopListCreateView.as_view(), name='shop-list-create'),
    path('shops/<int:pk>/', views.ShopDetailView.as_view(), name='shop-detail'),
    path('shops/<int:pk>/update/', views.ShopUpdateView.as_view(), name='shop-update'),
    path('shops/<int:pk>/delete/', views.ShopDeleteView.as_view(), name='shop-delete'),
    
    # Product management endpoints
    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('products/bulk-upload/', views.ProductBulkUploadView.as_view(), name='product-bulk-upload'),
    
    # Order management endpoints
    path('orders/', views.SellerOrderListView.as_view(), name='seller-order-list'),
    path('orders/<int:pk>/', views.SellerOrderDetailView.as_view(), name='seller-order-detail'),
    path('orders/<int:pk>/status/', views.OrderStatusUpdateView.as_view(), name='order-status-update'),
    path('orders/<int:pk>/ship/', views.OrderShipView.as_view(), name='order-ship'),
    
    # Analytics and reports
    path('analytics/', views.SellerAnalyticsView.as_view(), name='seller-analytics'),
    path('analytics/sales/', views.SalesAnalyticsView.as_view(), name='sales-analytics'),
    path('analytics/products/', views.ProductAnalyticsView.as_view(), name='product-analytics'),
    path('analytics/customers/', views.CustomerAnalyticsView.as_view(), name='customer-analytics'),
    
    # Inventory management
    path('inventory/', views.InventoryListView.as_view(), name='inventory-list'),
    path('inventory/<int:pk>/', views.InventoryDetailView.as_view(), name='inventory-detail'),
    path('inventory/<int:pk>/update/', views.InventoryUpdateView.as_view(), name='inventory-update'),
    path('inventory/low-stock/', views.LowStockAlertView.as_view(), name='low-stock-alert'),
    
    # Category management
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
] 