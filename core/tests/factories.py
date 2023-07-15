import factory
from cafes.models import Cafe, Review, BusinessDays, CafeOption, CafeBusinessHours
from filters.models import City, Filter, Option
from users.models import User


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City

    name = factory.Sequence(lambda n: "City_%d" % n)
    map = factory.Faker('url')
    slug = factory.Sequence(lambda n: "test_slug_%d" % n)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "username_%d" % n)
    name = factory.Sequence(lambda n: "User_%d" % n)
    age = factory.Faker("random_int", min=1, max=100)
    gender = factory.Iterator(['Male', 'Female'])


class BusinessDaysFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BusinessDays

    day = factory.Sequence(lambda n: "day_%d" % n)


class FilterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Filter

    name = factory.Sequence(lambda n: "Filter_%d" % n)
    city = factory.SubFactory(CityFactory)
    slug = factory.Sequence(lambda n: "test_slug_%d" % n)


class OptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Option

    name = factory.Sequence(lambda n: "Option_%d" % n)
    filter = factory.SubFactory(FilterFactory)
    slug = factory.Sequence(lambda n: "test_slug_%d" % n)


class CafeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cafe

    name = factory.Sequence(lambda n: "Cafe_%d" % n)
    address = factory.Sequence(lambda n: "Address_%d" % n)
    img = factory.Faker('image_url')
    city = factory.SubFactory(CityFactory)
    slug = factory.Sequence(lambda n: f"cafe-{n}")

    @factory.post_generation
    def options(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.cafe_option.add(*extracted)

    @factory.post_generation
    def business_hours(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.business_hours.add(*extracted)


class CafeOptionFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = CafeOption

    cafe = factory.SubFactory(CafeFactory)
    cafe_option = factory.SubFactory(OptionFactory)
    rating = factory.Faker("random_int", min=0, max=2)
    sum_user = factory.Faker("random_int", min=1)
    sum_rating = factory.Faker("random_int", min=0)


class CafeBusinessHoursFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = CafeBusinessHours

    cafe = factory.SubFactory(CafeFactory)
    business_days = factory.SubFactory(BusinessDaysFactory)
    business_hours = factory.Sequence(lambda n: "hours_%d" % n)


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    cafe = factory.SubFactory(CafeFactory)
    user = factory.SubFactory(UserFactory)
    cafe_option = factory.SubFactory(CafeOptionFactory)
    rating = factory.Faker("random_int", min=0, max=2)
    reviews = factory.Faker("text")
