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
    cpf_cnpj = models.CharField(_("description"), max_length=14, unique=True)
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

    business = models.ForeignKey(
        Business, models.CASCADE, related_name="business_service"
    )
    price_hours = models.FloatField(_("estimated price per hour"))
    business_category = models.ForeignKey(BusinessCategory, models.CASCADE)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
