from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class PaymentInvoice(models.Model):
    parking_number = models.IntegerField()
    price = models.IntegerField()  # цена за парковочное место
    enrollment = models.IntegerField(default=0)  # зачисление
    accrual_date = models.DateField(auto_now_add=True)  # дата выставления счета выставляется автомотически при создании
    payment_date = models.DateField(auto_now=True)  # дата последнего зачисления (выст. при ласт обновлении таблицы)
    car = models.ForeignKey('Car', on_delete=models.CASCADE, null=True, related_name='invoices')

    def __str__(self):
        return f"{self.pk}: [{self.accrual_date}] [{self.payment_date}]"

    def display_debt(self):
        return str(self.car.debt)

    class Meta:
        verbose_name = 'Счет на оплату'
        verbose_name_plural = 'Счета на оплату'
        ordering = ['id']


class ParkingSpace(models.Model):
    number = models.IntegerField(unique=True)  # номер парковочного места
    price = models.IntegerField()
    is_occupied = models.BooleanField(default=False)
    car = models.OneToOneField('Car', on_delete=models.SET_NULL, blank=True, null=True, related_name='parking_space')

    def __str__(self):
        return str(self.number)

    def get_absolute_url(self):
        return reverse('parking_space', kwargs={'sp_id': self.pk})

    class Meta:
        verbose_name = 'Парковочное место'
        verbose_name_plural = 'Парковочные места'
        ordering = ['number']


class Car(models.Model):
    number = models.CharField(max_length=20)
    brand = models.CharField(max_length=70)  # марка авто
    clients = models.ManyToManyField('Client', related_name='cars')
    debt = models.IntegerField(default=0)  # долг на этой машине
    # space = models.OneToOneField(ParkingSpace, on_delete=models.SET_NULL)  # надо ли это поле тут

    def __str__(self):
        return self.number

    def get_absolute_url(self):
        return reverse('car', kwargs={'car_id': self.pk})

    def display_client(self):
        return ', '.join([client.name for client in self.clients.all()[:3]])

    def display_debt(self):
        return str(self.debt)

    display_client.short_description = 'Clients'

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ['id']


class Client(models.Model):
    name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    # cars = models.ManyToManyField(Car)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь',
                                related_name='client')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('client', kwargs={'client_id': self.pk})

    def display_cars(self):
        return ', '.join([car.number for car in self.cars.all()[:3]])

    display_cars.short_description = 'Cars'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['name']


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    short_description = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to="news_images/%Y/%m/%d/")

    def get_absolute_url(self):
        return reverse('article', kwargs={'news_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['title']


class Question(models.Model):
    content = models.TextField()
    answer = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['time_create']


class Vacancy(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['name']


class Review(models.Model):
    username = models.CharField(max_length=255)
    mark = models.IntegerField()
    content = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-time_create']


class Coupon(models.Model):
    code = models.CharField(max_length=255)
    description = models.TextField()
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'
        ordering = ['code']


class Employee(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    description = models.TextField()
    telephone = models.CharField(max_length=20)
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['name']
