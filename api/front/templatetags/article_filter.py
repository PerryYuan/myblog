# coding:utf8
from django import template
import uuid
import json
register = template.Library()

@register.filter
def get_value(value,type_name):
    return json.loads(value)[type_name]
