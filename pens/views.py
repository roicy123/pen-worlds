from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import  CartItem, Product
from .forms import ProductForm, UserCreationForm
from django.contrib.auth.models import User



def login_view(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if username == "admin" and password == "admin":
      return redirect('home')
    if user is not None:
      login(request, user)
      return redirect('product_list')
    else:
      return HttpResponse("<script>alert('Username or Password is incorrect');window.location='../login';</script>")
  return render(request, 'login.html')

# User Register


from django.shortcuts import render, redirect
from .forms import UserCreationForm, UserProfileInfoForm
from django.contrib import messages

def register_request(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = UserProfileInfoForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()  # refresh the user object to get the auto-generated password
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')
        else:
            return HttpResponse("<script>alert('Please enter valid details. Please check password or Username already exists.');window.location='../register';</script>")
    else:
        user_form = UserCreationForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})


# User Logout
@login_required
def logout_view(request):
  logout(request)
  return redirect('login')

# Home Page
@login_required
def home(request):
  products = Product.objects.all()
  return render(request, 'home.html', {'products': products})

# Add Product

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product_name = form.cleaned_data['name']
            
            # Check if a product with the same name already exists
            if Product.objects.filter(name=product_name).exists():
                messages.error(request, f'A product with the name "{product_name}" already exists.')
                return redirect('add_product')
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

# Edit Product
@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            quantity_increment = int(request.POST.get('quantity_increment', 0))
            if quantity_increment >= 0:
                product.quantity += quantity_increment
            form.save()
            messages.success(request, 'Product edited successfully!')
            return redirect('home')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form})


# Delete Product
@login_required
def delete_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('home')
    return render(request, 'delete_product.html', {'product': product})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})



@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})
 
@login_required
def add_to_cart(request, product_id): 
    product = Product.objects.get(id=product_id) 
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id) 
        if product.quantity > 0: 
            cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user) 
            if cart_item.quantity < product.quantity:
                cart_item.quantity += 1 
                cart_item.save()
        else:
            return HttpResponse("<script>alert('Product is not available at the moment.');window.location='/products/';</script>")
        return redirect('view_cart')
    else:
        messages.error(request, 'Please log in to add items to your cart.')
        return redirect('login')
 
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    product = cart_item.product
    if cart_item.quantity == 1: # check if the quantity is 1, not 0
        cart_item.delete()
    else:
        cart_item.quantity -= 1 # decrease the quantity by 1
        cart_item.save()

    return redirect('view_cart')


def product_list(request):
    query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    price_range = request.GET.get('price_range', '')
    
    # Start with all products
    products = Product.objects.all()
    
    # Filter by search query if provided
    if query:
        products = products.filter(name__icontains=query)
    
    # Filter by category if provided
    if category:
        if category == '1':
            products = products.filter(category=1)
        elif category == '2':
            products = products.filter(category=2)
        elif category == '3':
            products = products.exclude(category__in=[1, 2])
    
    # Filter by price range if provided
    if price_range:
        try:
            min_price, max_price = map(int, price_range.split('-'))
            products = products.filter(price__range=[min_price, max_price])
        except ValueError:
            # Handle invalid price range input
            pass

    # Check if no products found
    no_products_found = not products.exists()
    
    return render(request, 'product_list.html', {
        'products': products,
        'query': query,
        'category': category,
        'price_range': price_range,
        'no_products_found': no_products_found
    })


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem
from .models import CartItem, Product, CheckoutInfo
from .forms import CheckoutForm

@login_required
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Check if the user already has a CheckoutInfo object
            try:
                checkout_info = CheckoutInfo.objects.get(user=request.user)
            except CheckoutInfo.DoesNotExist:
                # If not, create a new CheckoutInfo object
                checkout_info = form.save(commit=False)
                checkout_info.user = request.user
                checkout_info.save()

            # Get the user's cart items
            cart_items = CartItem.objects.filter(user=request.user)
            total_price = sum(item.product.price * item.quantity for item in cart_items)

            return render(request, 'purchase_confirmation.html', {'user': request.user, 'cart_items': cart_items, 'total_price': total_price})
    else:
        form = CheckoutForm()
    return render(request, 'checkout.html', {'form': form})

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import PenCategory

def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        new_category = PenCategory(name=name)
        new_category.save()
        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, 'add_category.html')
from django.shortcuts import render, redirect
from .models import CartItem, Product
from django.contrib import messages
from .models import Order, OrderItem
from django.core.mail import send_mail
from django.conf import settings

def confirm_purchase(request):
    # Get the user's cart items
    cart_items = CartItem.objects.filter(user=request.user)

        # Create a new order
    order = Order.objects.create(user=request.user)

    # Update product quantities and remove items from the cart
    for item in cart_items:
        product = item.product
        quantity = item.quantity   
        product.quantity = product.quantity - quantity 
        product.save()
        # Add items to the order
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.price * cart_item.quantity
        )
        subject = 'Order Confirmation'
        message = f'Dear {request.user.get_full_name()},\n\nThank you for your order. Your order details are as follows:\n\nOrder ID: {order.id}\n\nWe will notify you when your order is shipped.\n\nBest regards,\nThe Pens Team'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.user.email]
        send_mail(subject, message, email_from, recipient_list)
    else:
        # If the product quantity is not sufficient, handle accordingly
        messages.warning(request, f"Product {product.name} is not available in sufficient quantity.")

        # Remove the item from the cart
        item.delete()
        
        # Implement this function to calculate total price

        # Redirect to the payment page with the total price
        return redirect('payment')
def thank_you_page(request):
    return render(request, 'thank_you.html')

from django.shortcuts import render
from django.views.generic import  DetailView
from .models import Product

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

from django.http import HttpResponseForbidden
def view_users(request):

    # Retrieve all users
    users = User.objects.all()

    # Render the user management template
    return render(request, 'view_users.html', {'users': users})

from django.shortcuts import render, redirect
from .models import Product, CartItem
from django.contrib import messages
@login_required
def buy_now(request, product_id):

    product = Product.objects.get(id=product_id)


    if product.quantity > 0:
        CartItem.objects.filter(user=request.user).delete()

        CartItem.objects.get_or_create(product=product, user=request.user, defaults={'quantity': 1})

    return redirect('checkout')


from .models import Product, UserReview
from .forms import UserReviewForm
@login_required
def add_review(request, product_id):
    if request.method == 'POST':
        form = UserReviewForm(request.POST)
        if form.is_valid():
            user_review = form.save(commit=False)
            user_review.product_id = product_id
            user_review.user = request.user
            user_review.save()
            return redirect('product_list')
    else:
        form = UserReviewForm()
    return render(request, 'add_review.html', {'form': form})

def product_reviews(request, product_id):
    product = Product.objects.get(id=product_id)
    reviews = UserReview.objects.filter(product=product)
    return render(request, 'reviews.html', {'reviews': reviews})

def first(request):
    products = Product.objects.all()
    return render(request, 'first.html', {'products': products})

def first(request):
    query = request.GET.get('search', '')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'first.html', {'products': products})

def first(request):
    query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.filter(name__icontains=query)
    
    return render(request, 'first.html', {'products': products, 'query': query, 'category': category})

def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Check if the provided username and password match the admin credentials
        if username == "admin" and password == "admin":
            # Log in the admin and redirect to the home page
            user, created = User.objects.get_or_create(username="admin")
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("<script>alert('Username or Password is incorrect');window.location='../admin_login';</script>")

    return render(request, 'admin_login.html')

def search_products(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'home.html', {'products': products})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfileInfo
from .forms import UserProfileInfoForm

@login_required
def edit_profile(request):
    user_profile = get_object_or_404(UserProfileInfo, user=request.user)
    if request.method == 'POST':
        form = UserProfileInfoForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # replace 'profile' with the name of your profile view
    else:
        form = UserProfileInfoForm(instance=user_profile)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def view_profile(request):
    user_profile = get_object_or_404(UserProfileInfo, user=request.user)
    return render(request, 'view_profile.html', {'user_profile': user_profile})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_history.html', {'orders': orders})


def manage_orders(request):
    orders = Order.objects.all()
    return render(request, 'manage_orders.html', {'orders': orders})


# views.py

def get_progress_percentage(status):
    status_mapping = {
        'PENDING': 0,
        'PROCESSING': 25,
        'SHIPPED': 65,
        'DELIVERED': 100,
        'CANCELLED': 0,  # Assuming cancelled orders do not progress
    }
    return status_mapping.get(status, 0)  # Default to 0 if status is not found

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    progress_percentage = get_progress_percentage(order.status)
    context = {
        'order': order,
        'progress_percentage': progress_percentage,
    }
    return render(request, 'order_detail.html', context)


from django.shortcuts import render, redirect
from .models import Order

def change_order_status(request, order_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order = Order.objects.get(id=order_id)
        order.status = new_status
        order.save()
        return redirect('manage_orders')
    else:
        # Handle GET request (if needed)
        pass

import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse



def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result, encoding='UTF-8')
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def download_invoice_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    user_profile = get_object_or_404(CheckoutInfo, user=request.user)
    order_items = order.orderitem_set.all()
    product_prices = {item.product.id: item.product.price for item in order.orderitem_set.all()}

    context = {
        'order': order,
        'user_profile': user_profile,
        'product_prices': product_prices,
    }

    template_path = 'download_invoice.html'
    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="invoice_{order_id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF')
    return response

from pens.management.commands.check_stock import Command as check_stock_command

def check_stock_view(request):
    # Execute the check_stock command
    check_stock_command().handle()

    # Return an HttpResponse object
    return HttpResponse("Check stock command executed you will recieve a notifiation shortly.")


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from django.core.mail import send_mail
from .forms import PasswordResetForm

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_link = f"{request.scheme}://{request.get_host()}/reset/{uid}/{token}/"
                send_mail(
                    'Password Reset',
                    f'Click the link to reset your password: {reset_link}',
                    '041129roycy@gmail.com',
                    [email],
                    fail_silently=False,
                )
                return redirect('password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset.html', {'form': form})

def password_reset_done(request):
    return render(request, 'password_reset_done.html')

from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect
from django.http import HttpResponse

UserModel = get_user_model()

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset_complete')
        else:
            form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        return HttpResponse('Invalid password reset link.')


def password_reset_complete(request):
    return render(request, 'password_reset_complete.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message, Supplier
from .forms import SupplierSendMessageForm,AdminSendMessageForm, AddSupplierForm
from .forms import SupplierLoginForm

from django.contrib.auth import authenticate, login
from django.contrib import messages

def supplier_login(request):
    if request.method == 'POST':
        form = SupplierLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.supplier:  # Assuming supplier is a related field in your User model
                    login(request, user)
                    # Redirect the supplier to the supplier home page
                    return redirect('supplier_home')
                else:
                    # User is not a supplier
                    return HttpResponse("<script>alert('You are authorized to access this page.');window.location='../logins/';</script>")
            else:
                # Invalid username or password
                return HttpResponse("<script>alert('Username or Password is incorrect');window.location='../logins/';</script>")
    else:
        form = SupplierLoginForm()
    return render(request,'supplier_login.html', {'form': form})


def supplier_home(request):
    if request.user.is_authenticated:
        supplier = request.user.supplier
        messages = Message.objects.filter(recipient=request.user)
        matching_products = Product.objects.filter(manufacture=supplier.company_name)
        

        return render(request, 'supplier_home.html', {'messages': messages, 'matching_products': matching_products})
    else:
        return redirect('login')

@login_required
def send_message(request):
    # Send message view logic
    if request.method == 'POST':
        form = SupplierSendMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('supplier_home')
    else:
        form = SupplierSendMessageForm()
    return render(request, 'send_message.html', {'form': form})

@login_required
def view_messages(request):
    # View messages view logic
    messages = Message.objects.filter(recipient=request.user)
    return render(request, 'view_messages.html', {'messages': messages})


@login_required
def add_supplier(request):
    if request.method == 'POST':
        form = AddSupplierForm(request.POST)
        if form.is_valid():
            # Create user
            user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            # Create supplier
            supplier = form.save(commit=False)
            supplier.user = user
            supplier.save()
            return redirect('home')
    else:
        form = AddSupplierForm()
    return render(request, 'add_supplier.html', {'form': form})

from .forms import EditSupplierForm

def edit_supplier(request, supplier_id):
    supplier = Supplier.objects.get(pk=supplier_id)
    if request.method == 'POST':
        form = EditSupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EditSupplierForm(instance=supplier)
    return render(request, 'edit_supplier.html', {'form': form})

def delete_supplier(request, supplier_id):
    supplier = Supplier.objects.get(pk=supplier_id)
    supplier.delete()
    return redirect('home')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def admin_send_message_view(request):
    if request.method == 'POST':
        form = AdminSendMessageForm(request.POST)
        if form.is_valid():
            form.instance.sender = request.user
            form.save()
            return redirect('admin_view_messages')  # Redirect to view messages page
    else:
        form = AdminSendMessageForm()
    return render(request, 'admin_send_message.html', {'form': form})

@login_required
def admin_view_messages_view(request):
    received_messages = Message.objects.filter(recipient=request.user)
    return render(request, 'admin_view_messages.html', {'received_messages': received_messages})

@login_required
def view_suppliers(request):
    suppliers = Supplier.objects.all()
    return render(request, 'view_suppliers.html', {'suppliers': suppliers})

# ...
from .forms import RefillRequest
from .forms import AdminSendRefillRequestForm
@login_required
def admin_send_refill_request(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    suppliers = Supplier.objects.all()
    if request.method == 'POST':
        form = AdminSendRefillRequestForm(request.POST)
        if form.is_valid():
            refill_request = form.save(commit=False)
            refill_request.product = product
            refill_request.save()
            return redirect('admin_view_refill_requests')
    else:
        form = AdminSendRefillRequestForm()
    return render(request, 'admin_send_refill_request.html', {'form': form, 'suppliers': suppliers, 'product': product})

@login_required
def admin_view_refill_requests(request):
    refill_requests = RefillRequest.objects.all()
    return render(request, 'admin_view_refill_requests.html', {'refill_requests': refill_requests})

@login_required
def supplier_view_refill_requests(request):
    refill_requests = RefillRequest.objects.filter(supplier=request.user.supplier)
    return render(request, 'supplier_view_refill_requests.html', {'refill_requests': refill_requests})

@login_required
def supplier_accept_refill_request(request, refill_request_id):
    refill_request = get_object_or_404(RefillRequest, id=refill_request_id)
    if refill_request.supplier == request.user.supplier:
        product = refill_request.product
        product.quantity += refill_request.quantity
        product.save()
        refill_request.status = 'ACCEPTED'
        refill_request.save()
        return redirect('supplier_view_refill_requests')
    else:
        return HttpResponseForbidden()

@login_required
def supplier_reject_refill_request(request, refill_request_id):
    refill_request = get_object_or_404(RefillRequest, id=refill_request_id)
    if refill_request.supplier == request.user.supplier:
        refill_request.status = 'REJECTED'
        refill_request.save()
        return redirect('supplier_view_refill_requests')
    else:
        return HttpResponseForbidden()

@login_required
def admin_audit_report(request):
    refill_requests = RefillRequest.objects.filter(status__in=['ACCEPTED', 'REJECTED'])
    return render(request, 'admin_audit_report.html', {'refill_requests': refill_requests})

def download_audit_report(request):
    refill_requests = RefillRequest.objects.all()
    context = {
        'refill_requests': refill_requests,
    }
    response = render_to_pdf('audit_report.html', context)
    response['Content-Disposition'] = 'attachment; filename="audit_report.pdf"'
    return response

# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order

@login_required
def process_payment(request):
    if request.method == 'POST':
        # Process the payment
        # (You can add your payment processing logic here)

        # Assuming the payment is successful, you might want to mark the order as paid
        # You should adjust this logic based on your application's requirements
        order = Order.objects.filter(user=request.user, status='pending').first()
        if order:
            order.status = 'paid'
            order.save()
            messages.success(request, 'Payment processed successfully!')
            return redirect('thank_you_page')
          # Redirect to order history page or any other relevant page
        else:
            messages.error(request, 'No pending orders found for payment.')
            return redirect('thank_you_page')  # Redirect to home page if there are no pending orders

    else:
        # If the request method is not POST, it's not a valid request
        messages.error(request, 'Invalid request method.')
        return redirect('payment')  # Redirect to home page if it's not a POST request



def payment(request):
        return render(request, 'payment.html')