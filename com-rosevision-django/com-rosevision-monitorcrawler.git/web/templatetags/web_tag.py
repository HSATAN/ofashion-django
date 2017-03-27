#! -*- coding:utf-8 -*-
from django.conf import settings
from django.template import Library
import json

register = Library()


@register.filter()
def json_get(dictionary, key):
    """字符串转dict，获得value"""
    return json.loads(dictionary).get(key)


@register.filter()
def string_to_list(string):
    """字符串转list"""
    return eval(string)


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()