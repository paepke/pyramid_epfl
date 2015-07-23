from solute.epfl.validators.number import NumberValidator

__author__ = 'juw'


class FloatValidator(NumberValidator):
    float = True  #: Just set this to True and NumberValidator will do the rest.
