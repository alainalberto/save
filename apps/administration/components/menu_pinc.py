from django.shortcuts import render_to_response

from django.utils.dateformat import format

from  apps.administration.models import Menus


def Menu_princ(request):


    return render_to_response('layout/layout.html', {})