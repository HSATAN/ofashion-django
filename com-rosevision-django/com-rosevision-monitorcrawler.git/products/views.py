# import json
# from django.http import HttpResponse
# import solr
# from mfashion_api import settings as api_settings
#
# __author__ = 'Zephyre'
#
#
# def query_products(request):
#     s = solr.SolrConnection(api_settings.SEARCH_ENGINE_URL)
#
#     start = int(request.GET.get('start', 0))
#     count = int(request.GET.get('count', 10))
#
#     q = request.GET.get('q')
#     if q:
#         ret = s.query(q, start=start, rows=count)
#     else:
#         name = request.GET.get('name')
#         model = request.GET.get('model')
#         desc = request.GET.get('desc')
#         details = request.GET.get('details')
#         tags = request.GET.get('tags')
#         brand = request.GET.get('brand')
#         query_list = []
#         if name:
#             query_list.append('name:%s' % name)
#         if model:
#             query_list.append('model:%s' % model)
#         if desc:
#             query_list.append('description:%s' % desc)
#         if details:
#             query_list.append('details:%s' % details)
#         if tags:
#             query_list.append('mfashion_tags:%s' % tags)
#         if brand:
#             query_list.append('brandname_e:%s' % brand)
#         ret = s.query(', '.join(query_list), start=start, rows=count)
#
#     results = {'total': ret.numFound, 'start': start, 'count': count, 'products': [tmp for tmp in ret]}
#
#     return HttpResponse(json.dumps({'status': True, 'results': results}),
#                         content_type='application/json; charset=utf-8')
