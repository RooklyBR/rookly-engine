from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.db import models
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from rookly.storages import AvatarUserMediaStorage


class UserManager(BaseUserManager):
    def _create_user(self, email, cpf, password=None, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        if not cpf:
            raise ValueError("The given cpf must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, cpf=cpf, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, cpf, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, cpf, password, **extra_fields)

    def create_superuser(self, email, cpf, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, cpf, password, **extra_fields)


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

    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)

    joined_at = models.DateField(_("joined at"), auto_now_add=True)

    photo = models.ImageField(
        _("photo user"), storage=AvatarUserMediaStorage(), null=True
    )

    objects = UserManager()

    @property
    def token_generator(self):
        return PasswordResetTokenGenerator()

    def check_password_reset_token(self, token):
        return self.token_generator.check_token(self, token)

    def make_password_reset_token(self):
        return self.token_generator.make_token(self)

    def send_welcome_email(self):
        if not settings.SEND_EMAILS:
            return False  # pragma: no cover
        context = {"name": self.first_name, "base_url": settings.BASE_URL}
        send_mail(
            _("Welcome to Rookly"),
            render_to_string("authentication/emails/welcome.txt", context),
            None,
            [self.email],
            html_message=render_to_string(
                "authentication/emails/welcome.html", context
            ),
        )

    def send_reset_password_email(self):
        if not settings.SEND_EMAILS:
            return False  # pragma: no cover
        token = self.make_password_reset_token()
        reset_url = "{}reset-password/{}/{}/".format(
            settings.ROOKLY_WEBAPP_BASE_URL, self.pk, token
        )
        context = {"reset_url": reset_url, "base_url": settings.BASE_URL}
        send_mail(
            _("Reset your Rookly password"),
            render_to_string("authentication/emails/reset_password.txt", context),
            None,
            [self.email],
            html_message=render_to_string(
                "authentication/emails/reset_password.html", context
            ),
        )


@receiver(models.signals.post_save, sender=User)
def send_welcome_email(instance, created, **kwargs):
    if created:
        instance.send_welcome_email()
