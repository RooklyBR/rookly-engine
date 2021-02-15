from django.test import TestCase
from django.db import IntegrityError

from .models import User


class AuthenticationTestCase(TestCase):
    def test_new_user(self):
        User.objects.create_user(
            email="fake@user.com",
            password="fake",
            address_cep="00000000",
            address_number=0,
            birth_date="1997-09-08",
        )

    def test_new_superuser(self):
        User.objects.create_superuser(
            email="fake@user.com",
            password="fake",
            address_cep="00000000",
            address_number=0,
            birth_date="1997-09-08",
        )

    def test_new_user_fail_without_email(self):
        with self.assertRaises(ValueError):
            User.objects._create_user(
                email="",
                password="fake",
                address_cep="00000000",
                address_number=0,
                birth_date="1997-09-08",
            )

    def test_new_superuser_fail_issuperuser_false(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="fake@user.com",
                password="fake",
                address_cep="00000000",
                address_number=0,
                birth_date="1997-09-08",
                is_superuser=False,
            )

    def test_user_unique_email(self):
        User.objects.create_user(
            email="user1@user.com",
            password="fake",
            address_cep="00000000",
            address_number=0,
            birth_date="1997-09-08",
        )
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email="user1@user.com",
                password="fake",
                address_cep="00000000",
                address_number=0,
                birth_date="1997-09-08",
            )
