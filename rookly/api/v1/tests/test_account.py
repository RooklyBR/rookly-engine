import json

from django.test import RequestFactory
from django.test import TestCase
from django.test.client import MULTIPART_CONTENT
from rest_framework import status

from rookly.authentication.models import User
from rookly.common.models import Business, City
from .utils import create_user_and_token
from ..account.views import ChangePasswordViewSet
from ..account.views import LoginViewSet
from ..account.views import MyUserProfileViewSet
from ..account.views import RegisterUserViewSet
from ..account.views import RequestResetPasswordViewSet
from ..account.views import ResetPasswordViewSet
from ..account.views import UserProfileViewSet


class LoginTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.password = "abcgq!!123"
        self.email = "user@user.com"

        user = User.objects.create(
            email=self.email,
            first_name="User",
            address_cep="00000000",
            address_number=0,
            birth_date="1997-09-08",
        )
        user.set_password(self.password)
        user.save(update_fields=["password"])

    def request(self, data):
        request = self.factory.post("/v2/account/login/", data)
        response = LoginViewSet.as_view({"post": "create"})(request)
        response.render()
        content_data = json.loads(response.content)
        return (response, content_data)

    def test_okay(self):
        response, content_data = self.request(
            {"username": self.email, "password": self.password}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", content_data.keys())

    def test_wrong_password(self):
        response, content_data = self.request(
            {"username": self.email, "password": "wrong"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RegisterUserTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def request(self, data):
        request = self.factory.post("/v2/account/register/", data)
        response = RegisterUserViewSet.as_view({"post": "create"})(request)
        response.render()
        content_data = json.loads(response.content)
        return (response, content_data)

    def test_okay(self):
        email = "fake@user.com"
        password = "abc!1234"
        response, content_data = self.request(
            {
                "email": email,
                "first_name": "Fake",
                "last_name": "fake",
                "password": password,
                "address_cep": "00000000",
                "address_number": 0,
                "birth_date": "1997-09-08",
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=email)
        self.assertTrue(user.check_password(password))

    def test_invalid_password(self):
        response, content_data = self.request(
            {
                "email": "fake@user.com",
                "first_name": "Fake",
                "last_name": "Fake",
                "password": "abc",
                "address_cep": "00000000",
                "address_number": 0,
                "birth_date": "1997-09-08",
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", content_data.keys())


class RequestResetPasswordTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.email = "user@user.com"

        User.objects.create(
            email=self.email,
            first_name="User",
            address_cep="00000000",
            address_number=0,
            birth_date="1997-09-08",
        )

    def request(self, data):
        request = self.factory.post("/v2/account/forgot-password/", data)
        response = RequestResetPasswordViewSet.as_view({"post": "create"})(request)
        response.render()
        content_data = json.loads(response.content or "null")
        return (response, content_data)

    def test_okay(self):
        response, content_data = self.request({"email": self.email})

    def test_email_not_found(self):
        response, content_data = self.request({"email": "nouser@fake.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", content_data.keys())


class ResetPasswordTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.user = User.objects.create(
            email="user@user.com",
            first_name="User",
            address_cep="00000000",
            address_number=0,
            birth_date="1997-09-08",
        )
        self.reset_password_token = self.user.make_password_reset_token()

    def request(self, pk, data):
        request = self.factory.post("/v2/account/reset-password/{}/".format(pk), data)
        response = ResetPasswordViewSet.as_view({"post": "update"})(request, pk=pk)
        response.render()
        content_data = json.loads(response.content or "null")
        return (response, content_data)

    def test_okay(self):
        new_password = "valid12!"
        response, content_data = self.request(
            self.user.pk,
            {"token": self.reset_password_token, "password": new_password},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user = User.objects.get(pk=self.user.pk)
        self.assertTrue(self.user.check_password(new_password))

    def test_invalid_token(self):
        response, content_data = self.request(
            self.user.pk, {"token": "112233", "password": "valid12!"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("token", content_data.keys())


class ChangePasswordTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user, self.user_token = create_user_and_token()
        self.password = "12555q!66"
        self.user.set_password(self.password)
        self.user.save(update_fields=["password"])

    def request(self, data, token):
        authorization_header = {"HTTP_AUTHORIZATION": "Token {}".format(token.key)}
        request = self.factory.post(
            "/v2/account/change-password/", data, **authorization_header
        )
        response = ChangePasswordViewSet.as_view({"post": "update"})(request)
        response.render()
        content_data = json.loads(response.content or "null")
        return (response, content_data)

    def test_okay(self):
        new_password = "kkl8&!qq"
        response, content_data = self.request(
            {"current_password": self.password, "password": new_password},
            self.user_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wrong_password(self):
        response, content_data = self.request(
            {"current_password": "wrong_password", "password": "new_password"},
            self.user_token,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("current_password", content_data.keys())


class ListUserProfileTestCase(TestCase):
    fixtures = [
        "./rookly/common/fixtures/categories.json",
        "./rookly/common/fixtures/states.json",
    ]

    def setUp(self):
        self.factory = RequestFactory()
        self.user, self.user_token = create_user_and_token()
        self.business = Business.objects.create(
            user=self.user,
            name="rookly",
            city=City.objects.all().first(),
            cpf_cnpj="00000000000",
            presentation="",
        )

    def request(self, pk):
        request = self.factory.get("/v2/account/user-profile/{}/".format(pk))
        response = UserProfileViewSet.as_view({"get": "retrieve"})(request, pk=pk)
        response.render()
        content_data = json.loads(response.content)
        return (response, content_data)

    def test_okay(self):
        response, content_data = self.request(self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content_data.get("email"), self.user.email)

    def test_not_exists(self):
        response, content_data = self.request("no_exists")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(content_data.get("detail"), "Not found.")


class ListMyProfileTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user, self.user_token = create_user_and_token()

    def request(self, token):
        authorization_header = {"HTTP_AUTHORIZATION": "Token {}".format(token.key)}
        request = self.factory.get("/v2/account/my-profile/", **authorization_header)
        response = MyUserProfileViewSet.as_view({"get": "retrieve"})(request)
        response.render()
        content_data = json.loads(response.content)
        return (response, content_data)

    def test_okay(self):
        response, content_data = self.request(self.user_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content_data.get("email"), self.user.email)


class DestroyMyProfileTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user, self.user_token = create_user_and_token()

    def request(self, token):
        authorization_header = {"HTTP_AUTHORIZATION": "Token {}".format(token.key)}
        request = self.factory.delete("/v2/account/my-profile/", **authorization_header)
        response = MyUserProfileViewSet.as_view({"delete": "destroy"})(request)
        response.render()
        return response

    def test_okay(self):
        response = self.request(self.user_token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class UserUpdateTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user, self.user_token = create_user_and_token()

    def request(self, user, data, token):
        authorization_header = {"HTTP_AUTHORIZATION": "Token {}".format(token.key)}
        request = self.factory.patch(
            "/v2/account/my-profile/",
            self.factory._encode_data(data, MULTIPART_CONTENT),
            MULTIPART_CONTENT,
            **authorization_header
        )
        response = MyUserProfileViewSet.as_view({"patch": "update"})(
            request, pk=user.pk, partial=True
        )
        response.render()
        content_data = json.loads(response.content)
        return (response, content_data)

    def test_okay(self):
        first_name = "Maceió - Alagoas"
        response, content_data = self.request(
            self.user, {"first_name": first_name}, self.user_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content_data.get("first_name"), first_name)
