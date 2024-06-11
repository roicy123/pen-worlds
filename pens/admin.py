from django.contrib import admin
from .models import  CartItem, CheckoutInfo, Order,OrderItem, PenCategory,  Product, UserProfileInfo, UserReview, Message, Supplier,RefillRequest
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','description', 'price', 'image','category','manufacture','quantity','colour'] 

admin.site.register(PenCategory)
admin.site.register(Product, ProductAdmin)
admin.site.register(CheckoutInfo)
admin.site.register(CartItem)
admin.site.register(UserReview)
admin.site.register(UserProfileInfo)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Message)
admin.site.register(Supplier)
admin.site.register(RefillRequest)