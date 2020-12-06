import re
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError


class CPFCNPJValidator(object):
    def __call__(self, value):
        reg = re.compile(
            r"([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})"
        )
        if not reg.match(value):
            raise ValidationError(_("Enter a valid CPF or CNPJ."))
