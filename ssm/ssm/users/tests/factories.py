from factory import DjangoModelFactory, Faker, RelatedFactory

from ssm.users.models import User


class UserFactory(DjangoModelFactory):

    class Meta:
        model = User

    email = Faker('email')
    is_staff = False
    is_superuser = False


class StaffUserFactory(UserFactory):
    is_staff = True
    is_superuser = True
