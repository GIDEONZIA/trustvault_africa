import factory
from factory.django import DjangoModelFactory
from apps.accounts.models import User
from apps.properties.models import Property, Unit
from apps.tenants.models import Lease

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    user_type = 'landlord'
    phone_number = factory.Sequence(lambda n: f'0700000{n:03d}')

class PropertyFactory(DjangoModelFactory):
    class Meta:
        model = Property
    owner = factory.SubFactory(UserFactory)
    name = factory.Faker('company')
    slug = factory.Faker('slug')
    city = 'Nairobi'
    property_type = 'apartment'

class UnitFactory(DjangoModelFactory):
    class Meta:
        model = Unit
    property = factory.SubFactory(PropertyFactory)
    unit_number = factory.Sequence(lambda n: f'Unit-{n}')
    unit_type = '1_bedroom'
    monthly_rent = 35000
    deposit_amount = 35000

class LeaseFactory(DjangoModelFactory):
    class Meta:
        model = Lease
    unit = factory.SubFactory(UnitFactory)
    tenant = factory.SubFactory(UserFactory, user_type='tenant')
    lease_number = factory.Sequence(lambda n: f'RF-2026-{n:04d}')
    start_date = '2026-01-01'
    end_date = '2026-12-31'
    monthly_rent = 35000
    payment_day = 5
