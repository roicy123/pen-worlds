from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError


class PenCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images', blank=True)
    quantity = models.IntegerField(default=0)
    manufacture = models.CharField(max_length=100, default="Gokuldas Gangwani")
    colour = models.CharField(max_length=100, default="Black")
    category = models.ForeignKey(PenCategory, on_delete=models.CASCADE, default="1")
    reorder_level = models.IntegerField(default=10) # Add this line

    def clean(self):
        # Ensure quantity and price are not negative
        if self.quantity < 0 or self.price <= 0:
            raise ValidationError("Quantity and price must be non-negative.")

    def save(self, *args, **kwargs):
        # Call clean method before saving
        self.clean()
        super().save(*args, **kwargs)

    def increase_quantity(self, quantity):
        self.quantity += quantity
        self.save()

    def __str__(self):
        return self.name


from django.contrib.auth.models import User
from django.db import models

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40,null=True)
    mobile = models.CharField(max_length=20,null=True)
    email = models.EmailField(max_length=255, unique=True)

    def __str__(self):
        return self.user.username

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    
 
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

class UserReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()

    

    def __str__(self):
        return self.review
    
class CheckoutInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    shipping_address = models.CharField(max_length=250)
    contact_info = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username
    

from django.db import models
from django.contrib.auth.models import User
from .models import Product

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    date_ordered = models.DateTimeField(auto_now_add=True)
    status_choices = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='PENDING')

    @property
    def total_price(self):
        return sum(item.price for item in self.orderitem_set.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        super().save(*args, **kwargs)

from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=100)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.company_name
    # Add more fields as needed

from django.db import models
from django.contrib.auth.models import User

class RefillRequest(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')], default='PENDING')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def get_status_display(self):
        return self.status