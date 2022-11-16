from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, permission_required
from mmaptsp2.models import Mmap, Beneficiary, Branchcode, Sccn
# from mmpaptsp2.models import Client, Clientaccountcode
from datetime import datetime, timedelta
import csv, io
import xlwt
from django.contrib import messages
import json


@login_required(login_url= '/users/login')
def index(request):
    user = request.user
    if user.can_selectbranch==False:
        mmap_list           =       Mmap.objects.filter(mmap_branch=user.user_branch).order_by('mmap_expired')
        mmap_expired        =       mmap_list.filter(expired_status="True")
        mmap_current        =       mmap_list.filter(expired_status="False")
        # mmap_final          =       mmap_current.all().order_by('mmap_expired')
        paginator           =       Paginator(mmap_current, 10) 
        page_number         =       request.GET.get('page') 
        mmap_final          =       paginator.get_page(page_number)
        context             =       {'page_obj': mmap_final, 'expcount': mmap_expired.all().count(), 
                                    'currentcount':mmap_current.all().count(), 'total': mmap_list.all().count()}
        return render (request, 'mmaptsp2/index.html', context)

    else:

        mmap_list           =       Mmap.objects.all().order_by('mmap_expired')
        mmap_expired        =       mmap_list.filter(expired_status="True")
        mmap_current        =       mmap_list.filter(expired_status="False")
        # mmap_final          =       mmap_current.all().order_by('mmap_expired')
        paginator           =       Paginator(mmap_current, 10)
        page_number         =       request.GET.get('page')
        mmap_final           =       paginator.get_page(page_number)
        context             =       {'page_obj': mmap_final,'expcount': mmap_expired.all().count(), 
                                    'currentcount':mmap_current.all().count(), 'total': mmap_list.all().count() }
        return render (request, 'mmaptsp2/index.html', context)
