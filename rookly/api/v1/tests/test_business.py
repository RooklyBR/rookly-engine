import json

from django.test import RequestFactory, TestCase
from django.test.client import MULTIPART_CONTENT
from rest_framework import status

from rookly.api.v1.business.views import BusinessViewSet, BusinessServiceViewSet
from rookly.api.v1.tests.utils import create_user_and_token
from rookly.common.models import Business, City, BusinessService, BusinessCategory, SubCategory


class CreateBusinessAPITestCase(TestCase):
    fixtures = [
        "./rookly/common/fixtures/categories.json",
        "./rookly/common/fixtures/states.json",
    ]

    def setUp(self):
        self.factory = RequestFactory()

        self.owner, self.owner_token = create_user_and_token("owner")
        self.user, self.user_token = create_user_and_token("user")

    def request(self, data, token=None):
        authorization_header = (
            {"HTTP_AUTHORIZATION": "Token {}".format(token.key)} if token else {}
        )

        request = self.factory.post(
            "/v1/business/control/", data, **authorization_header
        )

        response = BusinessViewSet.as_view({"post": "create"})(request)
        response.render()
        content_data = json.loads(response.content)
        return (response, content_data)

    def test_okay(self):
        response, content_data = self.request(
            {
                "name": "string",
                "cpf_cnpj": "00000000000",
                "city": 1,
                "presentation": "string",
                "type_user": 0,
            },
            self.owner_token,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        business = self.owner.business.get(uuid=content_data.get("uuid"))

        self.assertEqual(business.name, content_data.get("name"))
        self.assertEqual(business.cpf_cnpj, "00000000000")


class UpdateBusinessTestCase(TestCase):
    fixtures = [
        "./rookly/common/fixtures/categories.json",
        "./rookly/common/fixtures/states.json",
    ]

    def setUp(self):
        self.factory = RequestFactory()

        self.owner, self.owner_token = create_user_and_token("owner")
        self.user, self.user_token = create_user_and_token("user")
        self.business = Business.objects.create(
            user=self.owner,
            name="rookly",
            city=City.objects.all().first(),
            cpf_cnpj="00000000000",
            presentation="",
        )

    def request(self, business, data={}, token=None):
        authorization_header = (
            {"HTTP_AUTHORIZATION": "Token {}".format(token.key)} if token else {}
        )

        request = self.factory.patch(
            "/v1/business/control/{}/".format(business.uuid),
            self.factory._encode_data(data, MULTIPART_CONTENT),
            MULTIPART_CONTENT,
            **authorization_header,
        )

        response = BusinessViewSet.as_view({"patch": "update"})(
            request, uuid=business.uuid, partial=True
        )
        response.render()
        content_data = json.loads(response.content)
        return (response, content_data)

    def test_okay_update_name(self):
        response, content_data = self.request(
            self.business,
            {"name": "Rookly {}".format(self.business.uuid)},
            self.owner_token,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized(self):
        response, content_data = self.request(
            self.business,
            {"name": "Rookly {}".format(self.business.uuid)},
            self.user_token,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DestroyBusinessTestCase(TestCase):
    fixtures = [
        "./rookly/common/fixtures/categories.json",
        "./rookly/common/fixtures/states.json",
    ]

    def setUp(self):
        self.factory = RequestFactory()

        self.owner, self.owner_token = create_user_and_token("owner")
        self.user, self.token = create_user_and_token()

        self.business = Business.objects.create(
            user=self.owner,
            name="rookly",
            city=City.objects.all().first(),
            cpf_cnpj="00000000000",
            presentation="",
        )

    def request(self, token):
        authorization_header = {"HTTP_AUTHORIZATION": "Token {}".format(token)}
        request = self.factory.delete(
            "/v1/business/control/{}/".format(str(self.business.uuid)),
            **authorization_header,
        )
        response = BusinessViewSet.as_view({"delete": "destroy"})(
            request, uuid=self.business.uuid
        )
        response.render()
        return response

    def test_okay(self):
        response = self.request(self.owner_token.key)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_private_okay(self):
        response = self.request("")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ListBusinessServiceTestCase(TestCase):
    fixtures = [
        "./rookly/common/fixtures/categories.json",
        "./rookly/common/fixtures/states.json",
    ]

    def setUp(self):
        self.factory = RequestFactory()

        self.owner, self.owner_token = create_user_and_token("owner")
        self.user, self.token = create_user_and_token()

        self.business = Business.objects.create(
            user=self.owner,
            name="rookly",
            city=City.objects.all().first(),
            cpf_cnpj="00000000000",
            presentation="",
        )
        self.business_category = self.business.business_category.create(
            subcategory=SubCategory.objects.all().first()
        )
        self.service = self.business.business_service.create(
            price=10.0,
            business_category=self.business_category
        )

    def request(self):
        request = self.factory.get(
            "/v1/business/service/"
        )
        response = BusinessServiceViewSet.as_view({"get": "list"})(
            request
        )
        response.render()
        content_data = json.loads(response.content)
        return (response, content_data)

    def test_okay(self):
        response, content_data = self.request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content_data["count"], 1)
        self.assertEqual(len(content_data["results"]), 1)
