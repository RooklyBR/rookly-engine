from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class State(models.Model):
    class Meta:
        verbose_name = _("state")
        unique_together = ["slug", "name"]

    slug = models.CharField(_("state slug"), max_length=255, null=False)
    name = models.CharField(_("state name"), max_length=255, null=False)

    def __str__(self):
        return self.name


class City(models.Model):
    class Meta:
        verbose_name = _("city")
        unique_together = ["state", "name"]

    state = models.ForeignKey(State, models.CASCADE)
    name = models.CharField(_("name city"), max_length=255, null=False)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def _create_user(self, email, cpf, city, password=None, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        if not cpf:
            raise ValueError("The given cpf must be set")
        if not city:
            raise ValueError("The given city must be set")

        email = self.normalize_email(email)
        city = City.objects.get(pk=city)
        user = self.model(email=email, cpf=cpf, city=city, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, cpf, city, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, cpf, city, password, **extra_fields)

    def create_superuser(self, email, cpf, city, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, cpf, city, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "cpf",
        "address_cep",
        "address_number",
        "address_complement",
        "birth_date",
        "city",
    ]

    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email"), unique=True, help_text=_("User's email."))
    cpf = models.CharField(
        _("cpf"), max_length=11, unique=True, help_text=_("User's cpf.")
    )
    telephone = models.CharField(
        _("telephone"), max_length=16, help_text=_("User's Telephone."), null=True
    )
    address_cep = models.IntegerField(_("cep"), help_text=_("User's Cep."))
    address_number = models.IntegerField(
        _("address number"), help_text=_("User's Address Number.")
    )
    address_complement = models.TextField(
        _("address complement"), help_text=_("User's Address Complement."), blank=True
    )
    birth_date = models.DateField(_("birth date"))

    city = models.ForeignKey(City, models.CASCADE)

    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)

    joined_at = models.DateField(_("joined at"), auto_now_add=True)

    objects = UserManager()

    @property
    def token_generator(self):
        return PasswordResetTokenGenerator()

    def check_password_reset_token(self, token):
        return self.token_generator.check_token(self, token)
