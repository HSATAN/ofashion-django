from django.shortcuts import render
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
import json
import base64
from Crypto.Cipher import AES
import MySQLdb

# Create your views here.
from configurations.models import HostConfiguration

__author__ = 'Zephyre'


def config(request, key):
    if request.method == 'GET':
        ret = HostConfiguration.objects.get(host_key=key)
        if ret.config_data:
            ret = {'config_data': json.loads(ret.config_data), 'status': True}
        else:
            ret = {'config_data': {}, 'status': True}
    elif request.method == 'PUT':
        data = json.dumps(json.loads(request.body))
        obj, created = HostConfiguration.objects.get_or_create(host_key=key,
                                                               defaults={'config_data': data, 'host_data': '{}'})
        if not created:
            obj.config_data = data
            obj.save()
        ret = json.dumps({'status': True})
    else:
        ret = {'status': False, 'reason': 'Invalid method: %s' % request.method}

    ret = json.dumps(ret)
    response = HttpResponse(ret, content_type='application/json; charset=utf-8')
    return response


def host_data(request, key):
    if request.method == 'GET':
        ret = HostConfiguration.objects.get(host_key=key)
        if ret.host_data:
            ret = {'host_data': json.loads(ret.host_data), 'status': True}
        else:
            ret = {'host_data': {}, 'status': True}
    elif request.method == 'PUT':
        data = json.dumps(json.loads(request.body))
        obj, created = HostConfiguration.objects.get_or_create(host_key=key,
                                                               defaults={'host_data': data, 'config_data': '{}'})
        if not created:
            obj.host_data = data
            obj.save()
        ret = json.dumps({'status': True})
    else:
        ret = {'status': False, 'reason': 'Invalid method: %s' % request.method}

    ret = json.dumps(ret)
    response = HttpResponse(ret, content_type='application/json; charset=utf-8')
    return response