import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class SchoolSessionValidator(RegexValidator):
    regex = re.compile(r'^\d{4}\\{1}\d{4}$')
    message='Enter a valid session in the format YYYY/YYYY eg 2000/2001.'

    def __call__(self, *args, **kwargs):
        super(SchoolSessionValidator, self).__call__(*args, **kwargs)

        value = args.get('value', '2001/2000')
        floor, ceiling = map(int, value.split('/'))
        if not (ceiling - floor) == 1:
            raise ValidationError

regex = re.compile(r'^\d{8,15}$')
PhoneNumberValidator = RegexValidator(regex=regex, message='Enter a valid telephone number.')
