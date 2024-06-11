
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import add_to_cart, admin_login_view, first, login_view, register_request, logout_view, home, add_product, edit_product, delete_product,product_list, remove_from_cart,view_cart


urlpatterns = [
    path('admin-login/', admin_login_view, name='admin_login'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home, name='home'),
    path('add-product/', add_product, name='add_product'),
    path('edit-product/<int:id>/', edit_product, name='edit_product'),
    path('delete-product/<int:id>/', delete_product, name='delete_product'),
    path('products/', product_list, name='product_list'),
    path("register", register_request, name="register"),
    path('cart/', view_cart, name='view_cart'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/',remove_from_cart, name='remove_from_cart'),
    path(' ',first, name='first'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

