#!-*- coding=utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django import forms
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.messages import constants as messages
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect

from django.contrib.auth import authenticate, login, logout


class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())


def login_view(request):
    if request.method == "POST":
        # user_form = UserForm(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                if 'next' in request.GET:
                    return HttpResponseRedirect(request.GET['next'])
                return render_to_response("tags/index.html", locals(), context_instance=RequestContext(request))
        else:
            error = 'error'
            return render_to_response("registration/login.html", locals(), context_instance=RequestContext(request))
    else:
        user_form = UserForm()
    return render_to_response("registration/login.html", locals(), context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    return render_to_response("registration/logout.html", locals(), context_instance=RequestContext(request))

def unauthenticated_view(request):
    return render_to_response("registration/unauthenticated.html", locals(), context_instance=RequestContext(request))

