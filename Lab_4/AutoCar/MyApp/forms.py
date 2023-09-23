from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import *
import re


class AddParkSpace(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['car'].empty_label = "Машина не выбрана"
        self.fields['car'].queryset = Car.objects.filter(parking_space__exact=None)
        self.fields['car'].label = 'Машина'
        self.fields['number'].label = 'Номер'
        self.fields['price'].label = 'Цена'
        self.fields['is_occupied'].label = 'Пометить как занятое'
        self.fields['is_occupied'].required = False

    class Meta:
        model = ParkingSpace
        fields = '__all__'

    def clean_number(self):
        num = self.cleaned_data['number']
        if num > 999 or num < 1:
            raise ValidationError('Номер парковочного места должен быть в диапазоне от 1 до 999')
        return num

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise ValidationError('Цена должна быть положительной')
        return price


class UpdatePrice(forms.Form):
    price = forms.IntegerField(label='Цена')

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise ValidationError('Цена должна быть положительной')
        return price


class PayForm(forms.Form):
    enrollment = forms.IntegerField(label='Сумма')

    def clean_enrollment(self):
        enrollment = self.cleaned_data['enrollment']
        if enrollment < 0:
            raise ValidationError('Зачисление должно быть положительное')
        return enrollment


def validate_age(value):  # проверка 18+
    today = timezone.now().date()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError("Вы должны быть старше 18 лет.")


def validate_phone_number(value):
    pattern = r'^\+375\(\d{2}\)\d{3}-\d{2}-\d{2}$'
    if not re.match(pattern, value):
        raise ValidationError("Неверный формат номера телефона. Используйте формат +375(XX)XXX-XX-XX.")


class RegisterUserForm(forms.Form):
    login = forms.CharField(max_length=100, label='Логин')
    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput, label='Введите пароль')
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput, label='Повторите пароль')
    email = forms.EmailField(label='эл. почта')
    name = forms.CharField(max_length=100, label='Ф.И.О.')
    telephone = forms.CharField(max_length=20, label='Телефон')
    date_of_birth = forms.DateField(validators=[validate_age], widget=forms.DateInput(attrs={'type': 'date'}), label='Дата Рождения')

    def clean_login(self):
        login = self.cleaned_data['login']
        try:
            user = User.objects.get(username=login)
        except:
            return login
        raise ValidationError('Пользователь с таким логином уже есть')

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
            raise ValidationError('Пороли не совпадают')

    def clean_telephone(self):
        telephone = self.cleaned_data['telephone']
        pattern = r'^\+375\(\d{2}\)\d{3}-\d{2}-\d{2}$'
        if not re.match(pattern, telephone):
            raise ValidationError("Неверный формат номера телефона. Используйте формат +375(XX)XXX-XX-XX.")
        else:
            return telephone

