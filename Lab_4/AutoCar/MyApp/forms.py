from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import *
import re

class AddParkSpace(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['car'].empty_label = "Car not selected"
        self.fields['car'].queryset = Car.objects.filter(parking_space__exact=None)
        self.fields['car'].label = 'Car'
        self.fields['number'].label = 'Number'
        self.fields['price'].label = 'Price'
        self.fields['is_occupied'].label = 'Mark as occupied'
        self.fields['is_occupied'].required = False

    class Meta:
        model = ParkingSpace
        fields = '__all__'

    def clean_number(self):
        num = self.cleaned_data['number']
        if num > 999 or num < 1:
            raise ValidationError('Parking space number should be between 1 and 999')
        return num

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise ValidationError('Price should be positive')
        return price

class UpdatePrice(forms.Form):
    price = forms.IntegerField(label='Price')

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise ValidationError('Price should be positive')
        return price

class PayForm(forms.Form):
    enrollment = forms.IntegerField(label='Amount')

    def clean_enrollment(self):
        enrollment = self.cleaned_data['enrollment']
        if enrollment < 0:
            raise ValidationError('Enrollment should be positive')
        return enrollment

def validate_age(value):
    today = timezone.now().date()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError("You must be older than 18.")

def validate_phone_number(value):
    pattern = r'^\+375\(\d{2}\)\d{3}-\d{2}-\d{2}$'
    if not re.match(pattern, value):
        raise ValidationError("Invalid phone number format. Use format +375(XX)XXX-XX-XX.")

class RegisterUserForm(forms.Form):
    login = forms.CharField(max_length=100, label='Username')
    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput, label='Enter password')
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput, label='Repeat password')
    email = forms.EmailField(label='Email')
    name = forms.CharField(max_length=100, label='Full Name')
    telephone = forms.CharField(max_length=20, label='Phone')
    date_of_birth = forms.DateField(validators=[validate_age], widget=forms.DateInput(attrs={'type': 'date'}), label='Date of Birth')

    def clean_login(self):
        login = self.cleaned_data['login']
        try:
            user = User.objects.get(username=login)
        except:
            return login
        raise ValidationError('User with this username already exists')

    def test_password(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 == password2:
            return True
        else:
            return False

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        if self.test_password():
            return password1
        else:
            raise ValidationError('Passwords do not match')

    def clean_telephone(self):
        telephone = self.cleaned_data['telephone']
        pattern = r'^\+375\(\d{2}\)\d{3}-\d{2}-\d{2}$'
        if not re.match(pattern, telephone):
            raise ValidationError("Invalid phone number format. Use format +375(XX)XXX-XX-XX.")
        else:
            return telephone