from django import forms
from .models import Product
from django.contrib.auth.models import User


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category','manufacture','quantity', 'image','colour']


import re
from django import forms
from django.contrib.auth.models import User
from .models import UserProfileInfo

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Password and confirm password do not match.")
            
            # Password strength validation
            if len(password) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long.")
            
        return cleaned_data
    
class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ('profile_pic','email','address','mobile')

# forms.py
from django import forms
from .models import Product, CartItem
from .models import CheckoutInfo
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = CheckoutInfo
        fields = ('first_name', 'last_name', 'shipping_address', 'contact_info')

    def clean(self):
        cleaned_data = super().clean()
        # You can add any custom validation logic here.
        return cleaned_data
    
from .models import UserReview

class UserReviewForm(forms.ModelForm):
    class Meta:
        model = UserReview
        fields = ['review']

class PasswordResetForm(forms.Form):
    email = forms.EmailField()

from django import forms
from .models import Message, Supplier

class AdminSendMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(AdminSendMessageForm, self).__init__(*args, **kwargs)
        # Filter the queryset for the recipient field to only include suppliers
        self.fields['recipient'].queryset = Supplier.objects.all()

class SupplierSendMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(SupplierSendMessageForm, self).__init__(*args, **kwargs)
        # Filter the queryset for the recipient field to only include admin users
        self.fields['recipient'].queryset = User.objects.filter(is_superuser=True)

class AddSupplierForm(forms.ModelForm):
    username = forms.CharField(max_length=150, help_text='Enter a username for the supplier')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Supplier                    
        fields = ['username', 'password', 'company_name', 'address', 'phone_number', 'email']


class SupplierLoginForm(forms.Form):
    username = forms.CharField(max_length=150, help_text='Enter your username')
    password = forms.CharField(widget=forms.PasswordInput, help_text='Enter your password')


class EditSupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier                    
        fields = ['company_name', 'address', 'phone_number', 'email']


from django import forms
from .models import RefillRequest

class AdminSendRefillRequestForm(forms.ModelForm):
    class Meta:
        model = RefillRequest
        fields = ['supplier', 'quantity','price']