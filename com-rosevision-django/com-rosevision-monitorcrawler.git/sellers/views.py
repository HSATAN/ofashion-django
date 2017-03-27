import MySQLdb
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection

# Create your views here.
from sellers.models import SellerRegistration


def get_seller_info(request, uid):
    uid = int(uid)
    seller_info = SellerRegistration.objects.get(uid=uid)
    ret_data = {'uid': uid, 'name': seller_info.name, 'email': seller_info.email,
                'date_of_birth': seller_info.date_of_birth.strftime('%Y-%m-%d'),
                'review_status': seller_info.review_status}
    ret = json.dumps(ret_data)
    response = HttpResponse(ret, content_type='application/json; charset=utf-8')
    response['Content-Length'] = len(ret)
    return response


def lookup_seller(request, name):
    cursor = connection.cursor()
    cursor.execute(
        'SELECT uid, name, email, date_of_birth, review_status FROM buyers_sellerregistration WHERE name LIKE "%%%s%%"' % MySQLdb.escape_string(
            name))
    rs = cursor.fetchall()
    ret_data = [
        {'uid': item[0], 'name': item[1], 'email': item[2], 'date_of_birth': item[3].strftime('%Y-%m-%d'),
         'review_status': item[4]} for item
        in rs]
    ret = json.dumps(ret_data)
    response = HttpResponse(ret, content_type='application/json; charset=utf-8')
    response['Content-Length'] = len(ret)
    return response


def update_seller(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        uid = int(data['uid'])

        seller_info = SellerRegistration.objects.get(uid=uid)

        name = data.get('name', None)
        email = data.get('email', None)
        date_of_birth = data.get('date_of_birth', None)
        review_status = data.get('review_status', None)

        if name:
            seller_info.name = name
        if email:
            seller_info.email = email
        if date_of_birth:
            seller_info.date_of_birth = date_of_birth
        if review_status:
            seller_info.review_status = review_status

        seller_info.save()
        return HttpResponse(json.dumps({'status': True}), content_type='application/json; charset=utf-8')
    elif request.method == 'PUT':
        data = json.loads(request.body)
        uid = int(data['uid'])
        name = data['name']
        email = data.get('email', '')
        date_of_birth = data.get('date_of_birth', '0001-01-01')
        review_status = data.get('review_status', 'WAITING')

        seller_info = SellerRegistration(uid=uid, name=name, email=email, date_of_birth=date_of_birth,
                                         review_status=review_status)
        seller_info.save()
        return HttpResponse(json.dumps({'status': True}), content_type='application/json; charset=utf-8')
    else:
        return HttpResponse(json.dumps({'status': False}), content_type='application/json; charset=utf-8')