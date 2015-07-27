#* coding: utf-8
from text import TextValidator
from email import EmailValidator
from number import NumberValidator
from float import FloatValidator
from youtube import YoutubeUrlValidator

TextValidator.register_name('text')
EmailValidator.register_name('email')
NumberValidator.register_name('number')
FloatValidator.register_name('float')
YoutubeUrlValidator.register_name('youtube_url')
