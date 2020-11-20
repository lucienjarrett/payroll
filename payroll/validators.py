from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


def nis_validator(value):
    nis = RegexValidator(r"[a-zA-Z]{1}\d{6}$", "Example of C893312.")
    return nis(value)


def trn_validator(value):
    trn = RegexValidator(r"^[^0$]",
                         "You should have 10 characters all numeric.")
    trn(value)
