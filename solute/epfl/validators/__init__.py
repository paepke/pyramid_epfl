from text import TextValidator
from email import EmailValidator
from number import NumberValidator
from float import FloatValidator

TextValidator.register_name('text')
EmailValidator.register_name('email')
NumberValidator.register_name('number')
FloatValidator.register_name('float')
