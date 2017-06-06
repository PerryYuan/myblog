# coding:utf8
from django import forms
import json

class BaseForm(forms.Form):
    def get_error(self):
        errors = json.loads(self.errors.as_json())
        errors_msg = ''
        for key, value in errors.iteritems():
            for msgs in value:
                errors_msg += msgs.get('message',None) + ','
        return errors_msg