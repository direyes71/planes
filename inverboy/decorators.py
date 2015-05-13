#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Diego Reyes

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.

from django.shortcuts import render_to_response, HttpResponseRedirect

from inverboy.models import Usuario
from inverboy.models import Proyecto

def user_is_logged(view):
    u"""Verifica si el usuario esta logueado"""
    @wraps(view)
    def check_user_is_logged(request, *args, **kwargs):
        if request.user.is_authenticated():
            request.session.set_expiry(600)
            return view(request, *args, **kwargs)
        return HttpResponseRedirect('/inverboy/')
    return check_user_is_logged


def user_has_permission(view, permission):
    u"""Verifica si el usuario esta tiene el permiso especificado"""
    @wraps(view)
    def check_user_has_permission(request, *args, **kwargs):
        if permission in request.user.get_all_permissions():
            return view(request, *args, **kwargs)
        return HttpResponseRedirect('/inverboy/home/')
    return check_user_has_permission


def user_has_permission(permission=None):
    def _user_has_permission(view):
        def _check_user_has_permission(request, *args, **kwargs):
            if permission in request.user.get_all_permissions():
                return view(request, *args, **kwargs)
            return HttpResponseRedirect('/inverboy/home/')
        return wraps(view)(_check_user_has_permission)
    return _user_has_permission


def user_is_member_project(view):
    u"""Verifica si el usuario es miembro de un proyecto"""
    @wraps(view)
    def check_user_is_member_project(request, *args, **kwargs):
        user = Usuario.objects.get(id=request.user.id)
        project = Proyecto.objects.get(id=kwargs['proyecto_id'])
        if project in user.lista_proyectos_vinculados():
            return view(request, *args, **kwargs)
        return HttpResponseRedirect('/inverboy/home/')
    return check_user_is_member_project