import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _

from rookly.authentication.models import User


class Category(models.Model):
    class Meta:
        verbose_name = _("category")

    name = models.CharField(_("name"), max_length=255)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    class Meta:
        verbose_name = _("subcategory")

    name = models.CharField(_("name"), max_length=255)
    category = models.ForeignKey(Category, models.CASCADE, related_name="subcategory")

    def __str__(self):
        return self.name


class State(models.Model):
    class Meta:
        verbose_name = _("state")
        unique_together = ['slug', 'name']

    slug = models.CharField(_("state slug"), max_length=255, null=False)
    name = models.CharField(_('state name'), max_length=255, null=False)

    def __str__(self):
        return self.name


class City(models.Model):
    class Meta:
        verbose_name = _("city")
        unique_together = ['state', 'name']

    state = models.ForeignKey(State, models.CASCADE)
    name = models.CharField(_('name city'), max_length=255, null=False)

    def __str__(self):
        return self.name


class Business(models.Model):
    class Meta:
        verbose_name = _("business")

    FREELANCER = 0
    BUSINESS = 1
    TYPE_USER_CHOICES = [(FREELANCER, _("FreeLancer")), (BUSINESS, _("Business"))]

    uuid = models.UUIDField(
        _("UUID"), primary_key=True, default=uuid.uuid4, editable=False
    )
    user = models.ForeignKey(User, models.CASCADE, related_name="business")
    name = models.CharField(_("name business"), max_length=255)
    city = models.ForeignKey(City, models.CASCADE)
    cpf_cnpj = models.CharField(_("cpf or cnpj"), max_length=14, unique=True)
    presentation = models.TextField(_("presentation"), blank=True)
    type_user = models.PositiveIntegerField(
        _("type user"), choices=TYPE_USER_CHOICES, default=FREELANCER
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)


class BusinessCategory(models.Model):
    class Meta:
        verbose_name = _("business category")
        unique_together = ["business", "subcategory"]

    subcategory = models.ForeignKey(SubCategory, models.CASCADE)
    business = models.ForeignKey(
        Business, models.CASCADE, related_name="business_category"
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)


class BusinessService(models.Model):
    class Meta:
        verbose_name = _("business service")

    PAYMENT_HOUR = "payment_hour"
    PAYMENT_SESSION = "payment_session"
    PAYMENT_DAILY = "payment_daily"
    TYPE_PAYMENT_CHOICES = [
        (
            PAYMENT_HOUR,
            _("Hour-based payment"),
        ),
        (
            PAYMENT_SESSION,
            _("Session-based payment"),
        ),
        (
            PAYMENT_DAILY,
            _("Daily-based payment"),
        ),
    ]

    business = models.ForeignKey(
        Business, models.CASCADE, related_name="business_service"
    )
    price = models.FloatField(_("price"))
    payment_type = models.CharField(
        _("payment type"),
        max_length=50,
        choices=TYPE_PAYMENT_CHOICES,
        default=PAYMENT_HOUR,
    )
    business_category = models.ForeignKey(BusinessCategory, models.CASCADE)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
