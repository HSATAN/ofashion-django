#-*- coding:utf-8 -*-
import datetime
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.template import RequestContext
from django.forms.models import modelformset_factory, formset_factory
from django.db.models import Q
import operator
from django.contrib.auth.models import User, Permission
import time
from web.models import *
from tags.forms import *
import re
import json
from django.contrib.auth.decorators import permission_required
from datetime import *

mfashion_tags_perm = 'products.change_mfashiontags'
tag_mapping_perm = 'products.change_originaltags'
custom_tags_perm = 'products.change_customtags'
gender_perm = 'products.change_gender'


@login_required()
@permission_required(gender_perm, login_url='/accounts/unauthenticated/')
def gender(request):
    #款式处理
    #男款 女款 其他
    brand = request.GET.get('brand', None)
    sort = request.GET.get('sort', None)
    search = request.GET.get('search', None)
    order = request.GET.get('order', None)
    mfashion = request.GET.get('mfashion', None)

    filter_brand = Q(brand_id=brand) if brand else ~Q(brand_id=None)

    if sort == '0':
        filter_sort = ~Q(gender='male') & ~Q(gender='female') & ~Q(gender='None')
    elif sort == 'male':
        filter_sort = Q(gender=sort)
    elif sort == 'female':
        filter_sort = Q(gender=sort)
    elif sort == 'None':
        filter_sort = Q(gender=sort)
    else:
        filter_sort = ~Q(brand_id=None)

    if mfashion == '0':
        filter_mfashion = Q(mfashion_tags=[])
    elif mfashion:
        filter_mfashion = Q(mfashion_tags__contains=mfashion)
    else:
        filter_mfashion = ~Q(brand_id=None)

    search_word = reduce(operator.and_, (
        (Q(custom_tags__icontains=x) | Q(name__icontains=x) | Q(description__icontains=x) | Q(details__icontains=x)) for x
        in
        search.split(' '))) if search else ~Q(
        brand_id=None)

    order_seq = '-update_time' if order == 'new' else 'update_time'

    current_url = request.get_full_path()

    is_gender = True

    home_url = re.findall(r'(/tags/\d+|/tags)', current_url)[0]

    #品牌下拉列表
    brand_name = ZOnlineScheduleInfo.objects.get(filter_brand).brandname_e if brand else None
    brands = ZOnlineScheduleInfo.objects.all().order_by('brandname_e')

    temp = [{'男款':'male'},{'女款':'female'}, {'其他':'None'}]

    mfashion_tags = MfashionTags.objects.all()  #类目处理

    if sort == '0':
        products_all = ProductsRelease.objects.filter(
            filter_brand, filter_mfashion, search_word).filter(gender__isnull = True).all().order_by(order_seq)
    else:
         products_all = ProductsRelease.objects.filter(
            filter_brand, filter_mfashion, filter_sort, search_word).all().order_by(order_seq)



    total = products_all.count()   #总数


    #分页
    limit = 120
    paginator = Paginator(products_all, limit)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    queryset = None
    queryset = products_all.filter(
        pk__in=[p.fingerprint for p in products.object_list]).all()

    if request.method == 'POST':
        formset = ReleaseFormSet2(request.POST or None, queryset=queryset)
        #update or add
        if formset.is_valid():
            for form in formset.forms:
                if request.POST.get(form.instance.pk, None) == '1':
                    fingerprint = form.initial['fingerprint']

                    last_gender = form.initial['gender']
                    current_gender = form.cleaned_data['gender']
                    save_current_gender = current_gender[0] if current_gender else ''
                    if last_gender is None:
                        last_custom_tags = []
                    else:
                        last_custom_tags = [last_gender]
                    current_custom_tags = list(current_gender)
                    user_id = request.user.id

                    ProductsRelease.objects.filter(fingerprint=fingerprint).update(gender=save_current_gender)

                    # ProductsRelease.objects.filter(fingerprint=fingerprint).update(gender=current_gender,
                    #                                                                has_processed=1)
                    TagMappingHistory(fingerprint=fingerprint, last_mfashion_tags=last_custom_tags,
                                      current_mfashion_tags=current_custom_tags, user_id=user_id, tag_type=2).save()
            return HttpResponseRedirect(current_url)
    else:
        formset = ReleaseFormSet2(queryset=queryset)

    return render_to_response("tags/gender.html", locals(), context_instance=RequestContext(request))


@login_required()
def tags(request):
    #类目处理
    #品牌、分类、是否处理、有无标签
    brand = request.GET.get('brand', None)
    sort = request.GET.get('sort', None)
    # processed = request.GET.get('processed', None)
    # has_tag = request.GET.get('has_tag', None)
    search = request.GET.get('search', None)
    order = request.GET.get('order', None)

    filter_brand = Q(brand_id=brand) if brand else ~Q(brand_id=None)
    # filter_sort = Q(mfashion_tags__contains=sort) if sort else ~Q(brand_id=None)

    if sort == '0':
        filter_sort = Q(mfashion_tags=[])
    elif sort:
        filter_sort = Q(mfashion_tags__contains=sort)
    else:
        filter_sort = ~Q(brand_id=None)

    # if has_tag == '1':
    #     filter_tag = ~Q(mfashion_tags=[])
    # elif has_tag == '0':
    #     filter_tag = Q(mfashion_tags=[])
    # else:
    #     filter_tag = ~Q(brand_id=None)

    # filter_processed = Q(has_processed=processed) if processed else ~Q(brand_id=None)
    search_word = reduce(operator.and_, (
        (Q(mfashion_tags__icontains=x) | Q(name__icontains=x) | Q(description__icontains=x) | Q(details__icontains=x)) for x
        in
        search.split(' '))) if search else ~Q(
        brand_id=None)
    order_seq = '-update_time' if order == 'new' else 'update_time'

    current_url = request.get_full_path()

    is_index = True
    # if re.findall(r'(/tags/*$|/tags/\?page|/tags/\?)', current_url):
    #     is_index = True
    # else:
    #     is_index = False

    home_url = re.findall(r'(/tags/\d+|/tags)', current_url)[0]

    #品牌下拉列表
    brand_name = ZOnlineScheduleInfo.objects.get(filter_brand).brandname_e if brand else None
    brands = ZOnlineScheduleInfo.objects.all().order_by('brandname_e')
    mfashion_tags = MfashionTags.objects.all()

    # products_all = ProductsRelease.objects.filter(
    #     filter_brand, filter_sort, filter_tag, filter_processed, search_word).all().order_by(order_seq)

    products_all = ProductsRelease.objects.filter(
        filter_brand, filter_sort, search_word).all().exclude(
        brand_id__in=[10006, 10114, 10032, 10040, 10085, 10100, 10113, 10127, 10138, 10155, 10169, 10241,
                      10299, 10322]).order_by(order_seq)

    #分页
    limit = 120
    paginator = Paginator(products_all, limit)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    queryset = None
    queryset = products_all.filter(
        pk__in=[p.fingerprint for p in products.object_list]).all()

    #标签提交post更新
    if request.method == 'POST':
        formset = ReleaseFormSet(request.POST or None, queryset=queryset)
        #update or add
        if formset.is_valid():
            for form in formset.forms:
                if request.POST.get(form.instance.pk, None) == '1':
                    # form.save()
                    fingerprint = form.initial['fingerprint']
                    last_mfashion_tags = form.initial['mfashion_tags']
                    current_mfashion_tags = form.cleaned_data['mfashion_tags']
                    user_id = request.user.id

                    ProductsRelease.objects.filter(fingerprint=fingerprint).update(mfashion_tags=current_mfashion_tags,
                                                                                   has_processed=1)
                    TagMappingHistory(fingerprint=fingerprint, last_mfashion_tags=last_mfashion_tags,
                                      current_mfashion_tags=current_mfashion_tags, user_id=user_id).save()
            return HttpResponseRedirect(current_url)
    else:
        formset = ReleaseFormSet(queryset=queryset)

    return render_to_response("tags/index.html", locals(), context_instance=RequestContext(request))


@login_required()
def custom_tags(request):
    #标签处理
    #品牌、分类、是否处理、有无标签
    brand = request.GET.get('brand', None)
    sort = request.GET.get('sort', None)
    search = request.GET.get('search', None)
    order = request.GET.get('order', None)
    mfashion = request.GET.get('mfashion', None)


    filter_brand = Q(brand_id=brand) if brand else ~Q(brand_id=None)

    if sort == '0':
        filter_sort = Q(custom_tags=[])
    elif sort:
        filter_sort = Q(custom_tags__contains=sort)
    else:
        filter_sort = ~Q(brand_id=None)

    if mfashion == '0':
        filter_mfashion = Q(mfashion_tags=[])
    elif mfashion:
        filter_mfashion = Q(mfashion_tags__contains=mfashion)
    else:
        filter_mfashion = ~Q(brand_id=None)

    search_word = reduce(operator.and_, (
        (Q(custom_tags__icontains=x) | Q(name__icontains=x) | Q(description__icontains=x) | Q(details__icontains=x)) for x
        in
        search.split(' '))) if search else ~Q(
        brand_id=None)
    order_seq = '-update_time' if order == 'new' else 'update_time'

    current_url = request.get_full_path()

    is_custom = True

    home_url = re.findall(r'(/tags/\d+|/tags)', current_url)[0]

    #品牌下拉列表
    brand_name = ZOnlineScheduleInfo.objects.get(filter_brand).brandname_e if brand else None
    brands = ZOnlineScheduleInfo.objects.all().order_by('brandname_e')
    custom_tags = CustomTags.objects.all()
    mfashion_tags = MfashionTags.objects.all()


    products_all = ProductsRelease.objects.filter(
        filter_brand, filter_mfashion, filter_sort, search_word).all().order_by(order_seq)

    total = products_all.count()   #总数


    #分页
    limit = 120
    paginator = Paginator(products_all, limit)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    queryset = None
    queryset = products_all.filter(
        pk__in=[p.fingerprint for p in products.object_list]).all()

    #标签提交post更新
    if request.method == 'POST':
        formset = ReleaseFormSet1(request.POST or None, queryset=queryset)
        #update or add
        if formset.is_valid():
            for form in formset.forms:
                if request.POST.get(form.instance.pk, None) == '1':
                    fingerprint = form.initial['fingerprint']
                    last_custom_tags = form.initial['custom_tags']
                    current_custom_tags = form.cleaned_data['custom_tags']
                    user_id = request.user.id

                    ProductsRelease.objects.filter(fingerprint=fingerprint).update(custom_tags=current_custom_tags,
                                                                                   has_processed=1)
                    TagMappingHistory(fingerprint=fingerprint, last_mfashion_tags=last_custom_tags,
                                      current_mfashion_tags=current_custom_tags, user_id=user_id,tag_type=1).save()
            return HttpResponseRedirect(current_url)
    else:
        formset = ReleaseFormSet1(queryset=queryset)

    return render_to_response("tags/index1.html", locals(), context_instance=RequestContext(request))



@login_required()
@permission_required(custom_tags_perm, login_url='/accounts/unauthenticated/')
def tags_manage(request):
    """标签管理"""
    if request.POST:
        instance = None
        if 'id' in request.POST:
            instance = get_object_or_404(CustomTags,idcustom_tags=request.POST['id'])
        form = CustomTagsForm(request.POST or None, instance=instance)

        if form.is_valid() and 'delete' in request.POST:
            model_instance = form.save(commit=False)
            model_instance.delete()
        elif form.is_valid():
            form.save()
    else:
        form = CustomTagsForm()

    all_forms = [CustomTagsForm(instance=val) for val in CustomTags.objects.all()]
    custom_tags = CustomTags.objects.all()

    return render_to_response("tags/tags_manage.html", locals(),
                              context_instance=RequestContext(request))


@login_required()
@permission_required(mfashion_tags_perm, login_url='/accounts/unauthenticated/')
def manage(request):
    #类目管理
    if request.POST:
        instance = None
        if 'id' in request.POST:
            instance = get_object_or_404(MfashionTags, idmfashion_tags=request.POST['id'])
        form = MfashionTagsForm(request.POST or None, instance=instance)

        #delete
        if form.is_valid() and 'delete' in request.POST:
            model_instance = form.save(commit=False)
            model_instance.delete()
        #update or add
        elif form.is_valid():
            form.save()
    else:
        form = MfashionTagsForm()

    all_forms = [MfashionTagsForm(instance=val) for val in MfashionTags.objects.all()]
    mfashion_tags = MfashionTags.objects.all()

    return render_to_response("tags/manage.html", locals(),
                              context_instance=RequestContext(request))


@login_required()
@permission_required(tag_mapping_perm, login_url='/accounts/unauthenticated/')
def mapping(request, brand=None):
    #标签映射
    brand_name = None
    if brand:
        products_all = ProductsRelease.objects.filter(brand_id=brand).all()
        brand_name = ZOnlineScheduleInfo.objects.get(brand_id=brand).brandname_e
        data = OriginalTags.objects.filter(brand_id=brand).filter(region__in=['cn', 'us', 'uk']).filter(
            tag_type__in=['category-0', 'category-1', 'category-2']).all().order_by('region', 'tag_type')
        #todo
        # tag_type__in=['category-0', 'category-1', 'category-2']).all().order_by('region', 'tag_type')
        forms = [OriginalTagsForm(instance=val) for val in data]
    else:
        products_all = ProductsRelease.objects.all()

    brands = ZOnlineScheduleInfo.objects.all().order_by('brandname_e')


    # OriginalTags.objects.filter(brand_id=10106).filter(region__in=['cn', 'us', 'uk']).all()

    return render_to_response("tags/mapping.html", locals(), context_instance=RequestContext(request))


#post data for tag-mapping,ajax
def mapping_ajax(request):
    if request.method == 'POST':
        instance = get_object_or_404(OriginalTags, idmappings=request.POST['idmappings'])
        form = OriginalTagsForm(request.POST or None, instance=instance)
        #update or add
        if form.is_valid():
            idmappings = form.cleaned_data['idmappings']
            brand_id = form.cleaned_data['brand_id']
            region = form.cleaned_data['region']
            tag_name = form.cleaned_data['tag_name']
            tag_type = form.cleaned_data['tag_type']
            mapping_tag1 = form.cleaned_data['mapping_tag1']
            mapping_tag2 = form.cleaned_data['mapping_tag2']
            mapping_tag3 = form.cleaned_data['mapping_tag3']
            mapping_list = json.dumps(filter(lambda x: x, [mapping_tag1, mapping_tag2, mapping_tag3]),
                                      ensure_ascii=False)
            OriginalTags.objects.filter(idmappings=idmappings).update(brand_id=brand_id, region=region,
                                                                      tag_name=tag_name,
                                                                      tag_type=tag_type, mapping_list=mapping_list,
                                                                      mapping_tag1=mapping_tag1,
                                                                      mapping_tag2=mapping_tag2,
                                                                      mapping_tag3=mapping_tag3, edited=1)
            # form.save()
            return HttpResponse(' '.join(filter(lambda x: x, [mapping_tag1, mapping_tag2, mapping_tag3])))
    return 'ERROR'


@login_required()
def record(request):
    #记录查询
    users = User.objects.all()
    year_list = [year for year in range(2014,2020)]
    month_list = [month for month in range(1,13)]
    day_list = [x for x in range(1,32)]

    if request.method == 'GET' and 'user' in request.GET:

        current_user = request.GET.get('user')  #获取id
        if current_user == '0':
            return render_to_response("tags/record.html", locals(), context_instance=RequestContext(request))
        elif current_user:
            user_obj = User.objects.get(pk=current_user)
            current_user_name = user_obj.username
            filter_user = Q(user_id__contains=user_obj.id)
        else:
            current_user_name= '所有用户'
            filter_user = ~Q(fingerprint=None)

        current_year = int(request.GET.get('current_time_year', None).encode('utf-8'))
        current_month = int(request.GET.get('current_time_month', None).encode('utf-8'))
        current_day = int(request.GET.get('current_time_day', None).encode('utf-8'))

        try:
            start_date = datetime(int(current_year), int(current_month), int(current_day), 0, 0, 0)
            end_date = datetime(int(current_year), int(current_month), int(current_day), 23, 59, 59)
        except ValueError:
            return render_to_response("tags/record.html", locals(), context_instance=RequestContext(request))


        history_all = TagMappingHistory.objects.filter(filter_user).filter(update_time__range=(start_date,end_date)).order_by('-update_time')

        for i in history_all:
            temp = ProductsRelease.objects.filter(fingerprint=i.fingerprint)  #品牌
            if temp.exists():
                brand = temp[0]
                i.id = brand.brandname_c

        finish_counts = TagMappingHistory.objects.filter(filter_user).\
            filter(update_time__range=(start_date,end_date)).count()

        total_counts = TagMappingHistory.objects.filter(filter_user).count()

        #分页
        limit = 100
        paginator = Paginator(history_all, limit)
        page = request.GET.get('page')
        try:
            history = paginator.page(page)
        except PageNotAnInteger:
            history = paginator.page(1)
        except EmptyPage:
            history = paginator.page(paginator.num_pages)

    return render_to_response("tags/record.html", locals(), context_instance=RequestContext(request))