import factory

from cafes.models import BusinessHours, Cafe, Review
from filters.models import City, Filter, Option
from users.models import User


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City

    name = factory.Sequence(lambda n: "City_%d" % n)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "username_%d" % n)
    name = factory.Sequence(lambda n: "User_%d" % n)
    age = factory.Faker("random_int", min=1, max=100)
    gender = factory.Iterator(["Male", "Female"])


class BusinessHoursFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BusinessHours

    mon = "09:00 - 23:00"
    tue = "09:00 - 23:00"
    wed = "09:00 - 23:00"
    thu = "09:00 - 23:00"
    fri = "09:00 - 23:00"
    sat = "09:00 - 23:00"
    sun = "09:00 - 23:00"


class CafeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cafe

    name = factory.Sequence(lambda n: "Cafe_%d" % n)
    address = factory.Sequence(lambda n: "Address_%d" % n)
    business_hours = factory.SubFactory(BusinessHoursFactory)
    img = factory.Faker("image_url")
    city = factory.SubFactory(CityFactory)
    # map = factory.Faker("url")


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    cafe = factory.SubFactory(CafeFactory)
    user = factory.SubFactory(UserFactory)
    rating = factory.Faker("random_int", min=0, max=2)
    content = factory.Faker("text")


class OptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Option

    name = factory.Sequence(lambda n: "Option_%d" % n)


class FilterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Filter

    name = factory.Sequence(lambda n: "Filter_%d" % n)
    option = factory.SubFactory(OptionFactory)
