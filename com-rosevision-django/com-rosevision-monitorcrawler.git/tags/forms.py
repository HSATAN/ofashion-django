# -*- coding:utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms.models import modelformset_factory
from web.models import MfashionTags, ProductsRelease, OriginalTags, CustomTags



class CustomTagsForm(ModelForm):
    idcustom_tags = forms.IntegerField(forms.HiddenInput, required=False)
    class Meta:
        model = CustomTags
        fields = ['idcustom_tags','tag','details']


class MfashionTagsForm(ModelForm):
    idmfashion_tags = forms.IntegerField(forms.HiddenInput, required=False)

    class Meta:
        model = MfashionTags
        fields = ['idmfashion_tags', 'tag', 'details']


class ReleaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReleaseForm, self).__init__(*args, **kwargs)
        self.fields['mfashion_tags'] = forms.MultipleChoiceField(
            choices=((val.tag, val.tag) for val in MfashionTags.objects.all()),
            widget=forms.CheckboxSelectMultiple)

    # mfashion_tags = forms.MultipleChoiceField(choices=((val.tag, val.tag) for val in MfashionTags.objects.all()),
    #                                           widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = ProductsRelease
        fields = ['fingerprint', 'mfashion_tags']


ReleaseFormsetBase = modelformset_factory(
    ProductsRelease, extra=0, fields=('fingerprint', 'mfashion_tags'))

ReleaseFormsetBase1 = modelformset_factory(
    ProductsRelease, extra=0, fields=('fingerprint', 'custom_tags'))

ReleaseFormsetBase2 = modelformset_factory(
    ProductsRelease, extra=0, fields=('fingerprint', 'gender'))


class ReleaseFormSet(ReleaseFormsetBase):
    # def __init__(self, *args, **kwargs):
    #     super(ReleaseFormSet, self).__init__(*args, **kwargs)
    #     self.fields['mfashion_tags'] = forms.MultipleChoiceField(
    #         choices=((val.tag, val.tag) for val in MfashionTags.objects.all()),
    #         widget=forms.CheckboxSelectMultiple)
    def add_fields(self, form, index):
        super(ReleaseFormSet, self).add_fields(form, index)
        form.fields['mfashion_tags'] = forms.MultipleChoiceField(
            choices=((val.tag, val.tag) for val in MfashionTags.objects.all()), required=False,
            widget=forms.CheckboxSelectMultiple)

class ReleaseFormSet1(ReleaseFormsetBase1):
    def add_fields(self, form, index):
        super(ReleaseFormSet1, self).add_fields(form, index)
        form.fields['custom_tags'] = forms.MultipleChoiceField(
            choices=((val.tag, val.tag) for val in CustomTags.objects.all()), required=False,
            widget=forms.CheckboxSelectMultiple)

class ReleaseFormSet2(ReleaseFormsetBase2):
    def add_fields(self, form, index):
        #temp ={'男款':'male', '女款':'female', '其他':'other'}
        temp = ['male', 'female', 'None']
        super(ReleaseFormSet2, self).add_fields(form, index)
        form.fields['gender'] = forms.MultipleChoiceField(
            choices=((v, v) for v in temp), required=False,
            widget=forms.CheckboxSelectMultiple)


class OriginalTagsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(OriginalTagsForm, self).__init__(*args, **kwargs)
        tag_choices = [('', '')] + list((val.tag, val.tag) for val in MfashionTags.objects.all())
        self.fields['mapping_tag1'] = forms.ChoiceField(
            choices=tag_choices, widget=forms.Select, required=False)
        self.fields['mapping_tag2'] = forms.ChoiceField(
            choices=tag_choices, widget=forms.Select, required=False)
        self.fields['mapping_tag3'] = forms.ChoiceField(
            choices=tag_choices, widget=forms.Select, required=False)

    idmappings = forms.IntegerField(widget=forms.HiddenInput(),required=False)
    brand_id = forms.CharField(label=u'品牌编号')
    region = forms.CharField(label=u'国家')
    tag_name = forms.CharField(label=u'标签名称')
    tag_type = forms.CharField(label=u'标签类型')
    mapping_list = forms.CharField(label=u'标签列表')
    # mapping_tag1 = forms.CharField(max_length=45, blank=True)
    # mapping_tag2 = forms.CharField(max_length=45, blank=True)
    # mapping_tag3 = forms.CharField(max_length=45, blank=True)

    class Meta:
        model = OriginalTags
        fields = ['idmappings', 'brand_id', 'region', 'tag_name', 'tag_type', 'mapping_list', 'mapping_tag1',
                  'mapping_tag2', 'mapping_tag3']
