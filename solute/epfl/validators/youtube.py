#* coding: utf-8
import re
from solute.epfl.validators.text import TextValidator



class YoutubeUrlValidator(TextValidator):
    def __init__(self, value='value', error_message='Youtube Url is invalid', *args, **kwargs):
        """Validate a related Input field as a valid youtube url.

        :param value: Where to get the value to be evaluated.
        :param error_message: Error message to be displayed upon failed validation.
        :param domain: List of domains accepted by this validator instance.
        :param error_message_domain: Error message to be displayed upon encountering a wrong domain.
        """
        super(YoutubeUrlValidator, self).__init__(value=value, error_message=error_message, *args, **kwargs)

    def validate(self, value=None, error_message=None,  **kwargs):
        result = super(YoutubeUrlValidator, self).validate(value=value, error_message=error_message, **kwargs)

        if result is False:
            return False

        if value is not None and value not in ["", u'']:
            youtube_match = re.compile(ur'(?:http(?:s)?:\/\/)?(?:www\.)?(?:m\.)?(?:youtu\.be\/|youtube\.com\/(?:(?:watch)?\?(?:.*&)?v(?:i)?=|(?:embed|v|vi|user)\/))([^\?&\"\'>]+)')
            match = re.search(youtube_match, value)
            if not match:
                self.error_message = error_message
                return False

        return True
