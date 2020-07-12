# Author: Abraham Yusuf <bb6xt@yahoo.com>
# Date: 3/28/12
# Time: 10:32 AM

from django.test import TestCase
from django.test.client import Client
from django.core.files import File
from django.conf import settings
from myproject.setup import forms

class SimpleTest(TestCase):
    def setUp(self):
        pass

    def test_school_form_is_multipart(self):
        client = Client()
        school_form_urls = ['/setup/school/', '/setup/school/edit/']
        enctype = 'enctype="multipart/form-data"'

        for url in school_form_urls:
            response = client.get(url)
            assert(enctype in response.content)

    def test_school_form_data_is_valid(self):
        logo = open('%s/setup/img/add.png' % settings.STATIC_ROOT)
        data = {'name': 'Landmark College', 'address': '5/11, Olayinka Ogunfile Street,Unity Estate, Owutu,',
                'city': 'Ikorodu', 'state': 'Lagos', 'phonenumber': '012876631', 'email': 'info@landmark-college.com',
                'website': 'http://www.landmark-college.com', 'principals_name': 'KonjaMan', 'logo': File(logo)}

        form = forms.SchoolForm(data=data)
        assert(form.is_valid())