import json

from django.test import RequestFactory, TestCase
from rest_framework import status

from rookly.api.v1.business.views import BusinessViewSet
from rookly.api.v1.tests.utils import create_user_and_token


class CreateRepositoryAPITestCase(TestCase):
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
