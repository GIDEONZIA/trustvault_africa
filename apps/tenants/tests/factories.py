import factory
from factory.django import DjangoModelFactory
from apps.accounts.models import User
from apps.properties.models import Unit, Property
from apps.tenants.models import Lease

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    user_type = 'landlord'

class LeaseFactory(DjangoModelFactory):
    class Meta:
        model = Lease
    
    # This automatically creates a unit and tenant when you call LeaseFactory()
    unit = factory.SubFactory('apps.properties.tests.factories.UnitFactory')
    tenant = factory.SubFactory(UserFactory, user_type='tenant')
    lease_number = factory.Sequence(lambda n: f'RF-2026-{n:04d}')
    start_date = '2026-01-01'
    end_date = '2026-12-31'
    monthly_rent = 35000
