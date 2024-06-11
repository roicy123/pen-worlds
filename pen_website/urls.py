"""
URL configuration for pen_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from pens import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.first, name='first'),
    path('products/',views.product_list),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('user/', include('pens.urls')),
    path('home/',views.home),
    path('login/',views.login_view),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('add-product/',views.add_product),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:id>/',views.delete_product),
    path("register/", views.register_request, name="register"),
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add_category/', views.add_category, name='add_category'),
    path('confirm-purchase/', views.confirm_purchase, name='confirm_purchase'),
    path('thank-you/', views.thank_you_page, name='thank_you_page'),
    path('view_users/', views.view_users, name='view_users'),
    path('buy_now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('add_review/<int:product_id>/', views.add_review, name='add_review'),
    path('product/<int:product_id>/reviews/', views.product_reviews, name='product_reviews'),
    path('search/', views.search_products, name='search_products'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('order-history/', views.order_history, name='order_history'),
    path('manage-orders/', views.manage_orders, name='manage_orders'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('change-order-status/<int:order_id>/', views.change_order_status, name='change_order_status'),
    path('download-invoice/<int:order_id>/', views.download_invoice_view, name='download-invoice'),
    path('check_stock/', views.check_stock_view, name='check_stock'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
    path('logins/', views.supplier_login, name='supplier_login'),
    path('homes/', views.supplier_home, name='supplier_home'),
    path('send_message/', views.send_message, name='send_message'),
    path('view_messages/', views.view_messages, name='view_messages'),
    path('add_supplier/', views.add_supplier, name='add_supplier'),
    path('send-message/', views.admin_send_message_view, name='admin_send_message'),
    path('view-messages/', views.admin_view_messages_view, name='admin_view_messages'),
    path('supplier-login/', views.supplier_login, name='supplier_login'),
    path('edit_supplier/<int:supplier_id>/', views.edit_supplier, name='edit_supplier'),
    path('delete_supplier/<int:supplier_id>/', views.delete_supplier, name='delete_supplier'),
    path('view_suppliers/', views.view_suppliers, name='view_suppliers'),
    path('send_refill_request/<int:product_id>/', views.admin_send_refill_request, name='admin_send_refill_request'),
    path('view_refill_request/', views.admin_view_refill_requests, name='admin_view_refill_requests'),
    path('view_refill_requests/', views.supplier_view_refill_requests, name='supplier_view_refill_requests'),
    path('accept_refill_request/<int:refill_request_id>/', views.supplier_accept_refill_request, name='supplier_accept_refill_request'),
    path('reject_refill_request/<int:refill_request_id>/', views.supplier_reject_refill_request, name='supplier_reject_refill_request'),
    path('audit-report/', views.admin_audit_report, name='admin_audit_report'),
    path('download_audit_report/', views.download_audit_report, name='download_audit_report'),
    path('payment/', views.payment, name='payment'),
    path('process_payment/', views.process_payment, name='process_payment')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)