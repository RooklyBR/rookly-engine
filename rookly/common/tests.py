from django.test import TestCase

from rookly.authentication.models import User
from rookly.common.models import BusinessService, Business, City, SubCategory


class BusinessServiceTestCase(TestCase):
    fixtures = [
        "./rookly/common/fixtures/categories.json",
        "./rookly/common/fixtures/states.json",
    ]

    def setUp(self):
        owner = User.objects.create_user(
            email="fake@user.com",
            password="123456",
            address_cep="00000000",
            address_number=0,
            birth_date="1997-09-08",
        )
        self.business = Business.objects.create(
            user=owner,
            name="rookly",
            city=City.objects.all().first(),
            cpf_cnpj="00000000000",
            presentation="",
        )
        self.business_category = self.business.business_category.create(
            subcategory=SubCategory.objects.all().first(),
        )
        self.business_service = BusinessService.objects.create(
            business=self.business, price=10.0, business_category=self.business_category
        )

    def test_business_service_ok(self):
        self.assertEqual(self.business_service.price, 10.0)

    def test_delete_category_service(self):
        category = self.business_category.pk
        self.business_service.delete()
        self.assertEqual(BusinessService.objects.filter(pk=category).count(), 0)
