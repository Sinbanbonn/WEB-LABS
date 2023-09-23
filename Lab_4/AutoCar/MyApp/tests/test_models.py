import pytest
from MyApp.models import *
from datetime import date


@pytest.fixture
def park_space(db) -> ParkingSpace:
    return ParkingSpace.objects.create(number=69, price=99)


@pytest.fixture
def user_one(db) -> User:
    return User.objects.create(username='test_name', password='123456')


@pytest.fixture
def client_one(db, user_one) -> Client:
    date_ber = date(2000, 6, 1)
    return Client.objects.create(name='Alex', telephone='+375(44)568-46-78', date_of_birth=date_ber, user=user_one)


@pytest.fixture
def car_one(db, client_one):
    return Car.objects.create(number='8888IP-7', brand='Audi')


@pytest.fixture
def invoice_one(db, car_one):
    date_ac = date(2022, 6, 1)
    date_pay = date(2022, 10, 1)
    return PaymentInvoice.objects.create(parking_number=10, price=100, accrual_date=date_ac,
                                         payment_date=date_pay, car=car_one)


def test_filter_park_space(park_space):
    assert ParkingSpace.objects.filter(number=69).exists()


def test_update_park_space(park_space):
    park_space.price = 100
    park_space.save()
    park_space_from_db = ParkingSpace.objects.get(number=69)
    assert park_space_from_db.price == 100


def test_default_value_space(park_space):
    assert not park_space.is_occupied


def test_filter_user_one(user_one):
    assert User.objects.filter(username='test_name').exists()


def test_filter_client(client_one):
    assert Client.objects.filter(name='Alex').exists()


def test_filter_car(car_one):
    assert Car.objects.filter(number='8888IP-7').exists()


def test_filter_invoice(invoice_one):
    assert PaymentInvoice.objects.filter(parking_number=10).exists()


def test_update_user(user_one):
    user_one.username = 'Vlad'
    user_one.save()
    user_one_from_db = User.objects.get(username='Vlad')
    assert user_one_from_db.username == 'Vlad'


def test_update_client_one(client_one):
    client_one.name = 'Name'
    client_one.save()
    client_one_db = Client.objects.get(name='Name')
    assert client_one_db.name == 'Name'


def test_update_car_one(car_one):
    car_one.number = '69696IP-7'
    car_one.save()
    cl = Car.objects.get(number='69696IP-7')
    assert cl.number == '69696IP-7'


def test_update_invoice(invoice_one):
    invoice_one.parking_number = 23
    invoice_one.save()
    db = PaymentInvoice.objects.get(parking_number=23)
    assert db.parking_number == 23


def test_update_invoice2(invoice_one):
    invoice_one.price = 123
    invoice_one.save()
    db = PaymentInvoice.objects.get(price=123)
    assert db.price == 123


def test_default_value_invoice(invoice_one):
    assert invoice_one.enrollment == 0


def test_test_default_value_car(car_one):
    assert car_one.debt == 0


def test_update_client_2(client_one):
    client_one.telephone = '+375(44)777-77-77'
    client_one.save()
    client_one_db = Client.objects.get(telephone = '+375(44)777-77-77')
    assert client_one_db.telephone == '+375(44)777-77-77'

