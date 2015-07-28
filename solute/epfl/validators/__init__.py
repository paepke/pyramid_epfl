#* coding: utf-8
from text import TextValidator
from email import EmailValidator
from number import NumberValidator
from float import FloatValidator
from streaming_video import StreamingVideoUrlValidator

TextValidator.register_name('text')
EmailValidator.register_name('email')
NumberValidator.register_name('number')
FloatValidator.register_name('float')
StreamingVideoUrlValidator.register_name("streaming_video_url")
