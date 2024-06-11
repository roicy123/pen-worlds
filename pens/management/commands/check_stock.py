from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.mail import send_mail
from pens.models import Product

class Command(BaseCommand):
    help = 'Checks stock levels and sends notifications for low stock levels'

    def handle(self, *args, **options):
        products = Product.objects.all()
        for product in products:
            if product.quantity <= product.reorder_level:
                # Send notification to admin
                subject = f'Product {product.name} has reached its reorder level'
                message = f'The quantity of {product.name} has reached its reorder level of {product.reorder_level}. Please reorder more.'
                email = '041129roycy@gmail.com' # Replace with your admin email address
                send_mail(subject, message, 'roicyvinu400@gmail.com', [email])
                self.stdout.write(self.style.SUCCESS(f'Notification sent for {product.name}'))