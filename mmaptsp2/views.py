from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, permission_required
from .models import Mmap, Beneficiary, Branchcode, Sccn
from clients.models import Client, Clientaccountcode
from datetime import datetime, timedelta
import csv, io
import xlwt
from django.contrib import messages
import json


# for PDF
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum



@login_required(login_url= '/users/login')
def index(request):
    user = request.user
    mmap_list           =       Mmap.objects.filter(is_canceled=False).order_by('mmap_expired')

    if user.can_selectbranch==False:
        mmap_list           =       mmap_list.filter(mmap_branch=user.user_branch)
    
    mmap_expired        =       mmap_list.filter(expired_status="True")
    mmap_current        =       mmap_list.filter(expired_status="False")
    # mmap_final          =       mmap_current.all().order_by('mmap_expired')
    paginator           =       Paginator(mmap_current, 10) 
    page_number         =       request.GET.get('page') 
    mmap_final          =       paginator.get_page(page_number)
    context             =       {'page_obj': mmap_final, 'expcount': mmap_expired.all().count(), 
                                'currentcount':mmap_current.all().count(), 'total': mmap_list.all().count()}
    return render (request, 'mmaptsp2/index.html', context)


    # if user.can_selectbranch==False:
    #     mmap_list           =       Mmap.objects.filter(mmap_branch=user.user_branch).order_by('mmap_expired')
    #     mmap_expired        =       mmap_list.filter(expired_status="True")
    #     mmap_current        =       mmap_list.filter(expired_status="False")
    #     # mmap_final          =       mmap_current.all().order_by('mmap_expired')
    #     paginator           =       Paginator(mmap_current, 10) 
    #     page_number         =       request.GET.get('page') 
    #     mmap_final          =       paginator.get_page(page_number)
    #     context             =       {'page_obj': mmap_final, 'expcount': mmap_expired.all().count(), 
    #                                 'currentcount':mmap_current.all().count(), 'total': mmap_list.all().count()}
    #     return render (request, 'mmaptsp2/index.html', context)

    # else:

    #     mmap_list           =       Mmap.objects.all().order_by('mmap_expired')
    #     mmap_expired        =       mmap_list.filter(expired_status="True")
    #     mmap_current        =       mmap_list.filter(expired_status="False")
    #     # mmap_final          =       mmap_current.all().order_by('mmap_expired')
    #     paginator           =       Paginator(mmap_current, 10)
    #     page_number         =       request.GET.get('page')
    #     mmap_final           =       paginator.get_page(page_number)
    #     context             =       {'page_obj': mmap_final,'expcount': mmap_expired.all().count(), 
    #                                 'currentcount':mmap_current.all().count(), 'total': mmap_list.all().count() }
    #     return render (request, 'mmaptsp2/index.html', context)

    # mmap_list = Mmap.objects.all().order_by('mmap_expired')
    # mmap_list = Mmap.objects.filter(expired_status="False")
    # paginator = Paginator(mmap_list, 10)    
    # page_number = request.GET.get('page')
    # mmap_list = paginator.get_page(page_number)
    # return render (request, 'mmaptsp2/index.html', {'page_obj': mmap_list})

@login_required(login_url= '/users/login')
def search(request):
    user = request.user
    term = request.GET.get('search', '')
    mmapraw         =       Mmap.objects.filter(expired_status="False").order_by('mmap_expired')
    mmap_list       =       mmapraw.filter(Q(mmap_name__icontains=term))

    if user.can_selectbranch==False:
        mmap_list   =       mmap_list.filter(mmap_branch=user.user_branch)

    paginator       =       Paginator(mmap_list, 10)    
    page_number     =       request.GET.get('page')
    mmap_list       =       paginator.get_page(page_number)
    return render (request, 'mmaptsp2/index.html', {'page_obj': mmap_list, 'term':term})


# def mmapdelete(request, mmap_id):
    # cycle           =       request.POST.get('client_cycle')
    # mmap        =       Mmap.objects.get(id=mmap_id)
    # Mmap.objects.filter(id=mmap_id).delete()    
    # Beneficiary.objects.get(mmapid=mmap_id).delete()
    # clientID.delete()
    
    # return HttpResponseRedirect('/mmaptsp2')
@login_required(login_url= '/users/login')
def mmapcancel(request, mmap_id):    
    mmap                    =   Mmap.objects.get(id=mmap_id)
    mmap.is_canceled        =   True
    mmap.expired_status     =   True
    mmap.save()
    return HttpResponseRedirect('/mmaptsp2')


@login_required(login_url= '/users/login')
def cancelledmmap(request):    
    user = user = request.user
    mmap_list =   Mmap.objects.filter(is_canceled=True)

    if user.can_selectbranch == False:
        mmap_list   =   mmap_list.filter(mmap_branch=user.user_branch)
    
    return render (request, 'mmaptsp2/cancelledmmap.html', {'page_obj': mmap_list})

@login_required(login_url= '/users/login')
def loadclient(request):
    user            =       request.user
    client_list     =       Client.objects.filter(client_isdisabled=False).order_by('-id')
    if user.can_selectbranch==False:
        client_list   =       client_list.filter(client_branch=user.user_branch)
    # client_list     =       Client.objects.filter(client_branch=user.user_branch).order_by('-id')
    paginator       =       Paginator(client_list, 10)    
    page_number     =       request.GET.get('page')
    client_list     =       paginator.get_page(page_number)
    return render (request, 'mmaptsp2/loadsearchclient.html', {'page_obj': client_list})

@login_required(login_url= '/users/login')
def searchclient(request):
    term = request.GET.get('search', '').strip()
    user = request.user

    activeClients = Client.objects.filter(client_isdisabled=False)

    if user.can_selectbranch == False:
        activeClients   =   activeClients.filter(client_branch=user.user_branch)
    # client_filter_branch    =   Client.objects.filter(client_branch=user.user_branch)
    client_list = activeClients.filter(Q(client_fname__icontains=term) | Q(client_lname__icontains=term)).order_by('-id')

    if term == "":
        paginator = Paginator(client_list, 5)    
        page_number = request.GET.get('page')
        client_list = paginator.get_page(page_number)
    return render (request, 'mmaptsp2/loadsearchclient.html', {'page_obj': client_list})


@login_required(login_url= '/users/login')
def addmmap(request, profile_id):    
    mmaptype =""

    client = Client.objects.get(pk=profile_id)       
    d_o_b = int((datetime.now().date() - client.client_dob).days / 365.25)

    if (d_o_b < 18):
        mmaptype = "N/A"
    elif (d_o_b < 65):
        mmaptype = "18-64"    
    elif d_o_b < 70 :
        mmaptype = "65-69"
    elif d_o_b > 70 :
        mmaptype = "70-Up"
    # else:
    #     mmaptype = "N/A"

    cycle= int(client.client_cycle) + 1
    context= {'client': client, 
                'd_o_b': str(d_o_b),
                'cycle':cycle,
                "mmaptype":mmaptype}
    return render(request, 'mmaptsp2/add.html', context) #with or w/o str it still working

@login_required(login_url= '/users/login')
def processaddmmap(request):

    hidclientid = request.POST.get('hidclientid')
    client = Client.objects.get(pk=hidclientid) 
    clientid=client.id
    client_code = client.client_code
    clientimg = client.client_image
    mmap_name = client.client_fname + " " + client.client_mname + " " + client.client_lname
    mmap_sex = client.client_gender
    mmap_age = int((datetime.now().date() - client.client_dob).days / 365.25)
    mmap_branch = client.client_branch
    mmap_address = client.client_address
    mmap_dob = client.client_dob
    client_cycle = int(client.client_cycle) + 1

    client.client_cycle = client_cycle
    client.save()
    
    if request.FILES.get('mmap_form_fimage'):
        mmap_form_fimage = request.FILES.get('mmap_form_fimage')
    else:
        mmap_form_fimage='mmaptsp2_pic/default_image.png'

    if request.FILES.get('mmap_form_bimage'):
        mmap_form_bimage = request.FILES.get('mmap_form_bimage')
    else:
        mmap_form_bimage='mmaptsp2_pic/default_image.png'

    mmap_setupdate = request.POST.get('mmap_setupdate')
    recuited_by = request.POST.get('recuited_by')        
    processed_by = request.POST.get('processed_by')
    processed_des = request.POST.get('processed_des')
    processed_date = request.POST.get('processed_date')
    checked_by = request.POST.get('checked_by')
    checked_des = request.POST.get('checked_des')
    checked_date = request.POST.get('checked_date')
    approved_by = request.POST.get('approved_by')
    approved_des = request.POST.get('approved_des')
    approved_date = request.POST.get('approved_date')
    mmap_type = request.POST.get('mmap_type')
    # mmap_form_fimage = request.POST.get('mmap_form_fimage')
    # mmap_form_bimage = request.POST.get('mmap_form_bimage')

    startDate = datetime.strptime(mmap_setupdate, '%Y-%m-%d')
    add1Year = datetime (startDate.year + 1, startDate.month, startDate.day)
    mmap_expired= add1Year #+ datetime.timedelta(days=1)
    #mmap_expired = mmap_setupdate + datetime.year(1)
    #mmap_expired = mmap_setupdate.days + 365.25
   

    # getclientcodes=get_object_or_404(Clientaccountcode, branch=client_branch)
    
    getbranchcode               = Branchcode.objects.get(bname=mmap_branch)
    branchcode                  = getbranchcode.bcode
    # client_branchcode           = getclientcodes.branchcode

    getbranchcodecount = Sccn.objects.filter(sccnbcode=branchcode)
    
    branchcodecounts    =   1
    zeros   =       '0'

    if getbranchcodecount:
        for getcounts in getbranchcodecount:
            branchcodecounts+=1   

    if branchcodecounts <= 9:
        zeros = '0000'
    
    elif branchcodecounts <= 99:
        zeros = '000'

    elif branchcodecounts <= 999:
        zeros = '00'
   
    elif branchcodecounts <= 9999:
        zeros = '0'
    
    else:
        zeros = ''


    sscnservicecentercontrolno         =           str(branchcode) + str(zeros) + str(branchcodecounts)


    mmap = Mmap.objects.create(clientid=clientid, mmap_name=mmap_name, mmap_sex=mmap_sex, mmap_age=mmap_age, mmap_branch=mmap_branch,
            mmap_address=mmap_address, mmap_setupdate=mmap_setupdate, recuited_by=recuited_by,  client_cycle=client_cycle,
            mmap_dob=mmap_dob, processed_by=processed_by, processed_des=processed_des, processed_date=processed_date,
            checked_by=checked_by, checked_des=checked_des, checked_date=checked_date, approved_by=approved_by,
            approved_des=approved_des, approved_date=approved_date, mmap_expired=mmap_expired,mmap_type=mmap_type, 
            clientimg=clientimg, mmap_form_fimage=mmap_form_fimage, mmap_form_bimage=mmap_form_bimage, mmapbcode=branchcode, mmapservicecentercontrolno=sscnservicecentercontrolno,
            client_code=client_code)
        
    mmap.save()

    sccn = Sccn.objects.create(sscnservicecentercontrolno=sscnservicecentercontrolno, 
                                sccnbcode=branchcode, sccnbranch=mmap_branch, client_name=mmap_name)
    sccn.save()


    # getidcount = Mmap.objects.only('id')
    # getidcount = str(Mmap.objects.latest('id'))

    mmapid = mmap.id
    mmapservicecentercontrolno  =   mmap.mmapservicecentercontrolno
    ben_mmap_name = mmap_name
    ben1 = request.POST.get('ben1')
    ben2 = request.POST.get('ben2')
    ben3 = request.POST.get('ben3')

    ben1_dob = request.POST.get('ben1_dob')
    if ben1_dob == "":
        ben1_dob = None

    ben2_dob = request.POST.get('ben2_dob')
    if ben2_dob == "":
        ben2_dob = None

    ben3_dob = request.POST.get('ben3_dob')
    if ben3_dob == "":
        ben3_dob = None

    ben1_rel = request.POST.get('ben1_rel')
    ben2_rel = request.POST.get('ben2_rel')
    ben3_rel = request.POST.get('ben3_rel')

    mmap_clientid = clientid
    client_cycle = request.POST.get('client_cycle')


    beneficiary = Beneficiary.objects.create(mmapid=mmapid, ben_mmap_name=ben_mmap_name, mmap_clientid=mmap_clientid, ben1=ben1, ben2=ben2, ben3=ben3, ben1_dob=ben1_dob,
        ben2_dob=ben2_dob, ben3_dob=ben3_dob, ben1_rel=ben1_rel, ben2_rel=ben2_rel, ben3_rel=ben3_rel, client_cycle=client_cycle,
        mmapservicecentercontrolno=mmapservicecentercontrolno)
    beneficiary.save()

    

    return HttpResponseRedirect('/mmaptsp2', {'mmap': mmap})

@login_required(login_url= '/users/login')
def mmapdetail(request, profile_id):
    try:
        mmap = Mmap.objects.get(pk=profile_id)  
        beneficiary = Beneficiary.objects.get(mmap_clientid=mmap.clientid, client_cycle=mmap.client_cycle)       
    except Client.DoesNotExist:
        raise Http404("Profile does not exist")
        
    return render(request, 'mmaptsp2/mmapdetail.html', {'mmap': mmap, 'beneficiary': beneficiary})

@login_required(login_url= '/users/login')
def mmapexpdetail(request, profile_id):
    expTrue = True
    try:
        mmap = Mmap.objects.get(pk=profile_id)  
        beneficiary = Beneficiary.objects.get(mmap_clientid=mmap.clientid, client_cycle=mmap.client_cycle)       
    except Client.DoesNotExist:
        raise Http404("Profile does not exist")
        
    return render(request, 'mmaptsp2/mmapdetailxp.html', {'mmap': mmap, 'beneficiary': beneficiary, 'expTrue':expTrue})

@login_required(login_url= '/users/login')
def mmapdetailpdf(request, profile_id):
    # _now = datetime.now()
    user = request.user
    exportresponse = HttpResponse(content_type='application/pdf')
    exportresponse['Content-Disposition'] = 'inline; attachment; filename=Mmap' + str(datetime.now())+'.pdf'
    exportresponse['Content-Transfer-Encoding'] = "binary"
    mmap = Mmap.objects.get(pk=profile_id)
    beneficiary = Beneficiary.objects.get(pk=profile_id, client_cycle=mmap.client_cycle) 
    # try:
    #     mmap = Mmap.objects.get(pk=profile_id)  
    #     beneficiary = Beneficiary.objects.get(pk=profile_id, client_cycle=mmap.client_cycle)       
    # except Client.DoesNotExist:
    #     raise Http404("Profile does not exist")
        
    # return render(request, 'mmaptsp2/outputpdfdetail.html', {'mmap': mmap, 'beneficiary': beneficiary, 'today': _now})
    context = {'mmap': mmap, 
                'beneficiary': beneficiary, 
                'user': user, 
                'today': datetime.now()}
    html_string = render_to_string('mmaptsp2/outputpdfdetail.html', context)
    html=HTML(string=html_string)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            #output = open(output.name, 'rb')
            output.seek(0)
            exportresponse.write(output.read())
    return exportresponse


@login_required(login_url= '/users/login')
def filterby(request):
    datestart = datetime.now()
    dateend = datetime.now()
    return render(request, 'mmaptsp2/filterby.html', {'datestart':datestart, 'dateend':dateend})

@login_required(login_url= '/users/login')
def processfilterby(request):
    
    datestart = request.GET.get('datestart')
    #datestart = datetime(2022, 5, 4)
    Fdatestart = datetime.strptime(datestart, '%Y-%m-%d')
    dateend = request.GET.get('dateend')
    #dateend = datetime(2022, 5, 14)
    Fdateend = datetime.strptime(dateend, '%Y-%m-%d')
    filtertype = request.GET.get('filtertype')
    user = request.user

    
    mmap_list           =       Mmap.objects.filter(expired_status="False")
    
    if user.can_selectbranch==False:
        mmap_list           =       mmap_list.filter(mmap_branch=user.user_branch)     

    if filtertype == "expired-date":
        mmap = mmap_list.filter(mmap_expired__range=[Fdatestart, Fdateend]).order_by('-mmap_expired')
    elif filtertype == "reg-date":
        mmap = mmap_list.filter(mmap_setupdate__range=[Fdatestart, Fdateend]).order_by('-mmap_setupdate')
    #mmap = Mmap.objects.filter(mmap_expired__range=[Fdatestart, Fdateend]).order_by('-mmap_expired')
    context = {'page_obj': mmap,
                'datestart':Fdatestart,
                'dateend': Fdateend,
                'filtertype': filtertype}
    return render(request, 'mmaptsp2/filterby.html', context)

@login_required(login_url= '/users/login')
def allexpcurrent(request, exporcurrent):
    user = request.user
    expTrue =   True
    
    # mmap_list               =       None

    if user.can_selectbranch:
        mmap_list           =       Mmap.objects.all()
    else:
        mmap_list           =       Mmap.objects.filter(mmap_branch=user.user_branch)       
    
    if exporcurrent     == 'exp':
        mmapfilter                =       mmap_list.filter(expired_status="True")
        status                    =       'Expired'
        expTrue                   =        True
    elif  exporcurrent  ==  'current':
        mmapfilter                =       mmap_list.filter(expired_status="False")
        status                    =       'Current'
        expTrue                   =        False

       
    return render(request, 'mmaptsp2/allexpcurrent.html', {'page_obj': mmapfilter, 'status': status})




@login_required(login_url= '/users/login')
def mmapclaim(request, mmap_id):
    pass

@login_required(login_url= '/users/login')
def mmapedit(request, mmap_id):
    try:
        mmap        = Mmap.objects.get(pk=mmap_id)  
        beneficiary = Beneficiary.objects.get(mmapid=mmap_id, client_cycle=mmap.client_cycle)       
    except Client.DoesNotExist:
        raise Http404("Profile does not exist")
        
    return render(request, 'mmaptsp2/mmapedit.html', {'mmap': mmap, 'beneficiary': beneficiary})

@login_required(login_url= '/users/login')
def patchsccn(request):
    
    mmaps=Mmap.objects.all().order_by('-id')


    try:
        for mmap in mmaps:
            if Beneficiary.objects.filter(mmap_clientid=mmap.clientid).filter(client_cycle=mmap.client_cycle).exists():
                beneficiary     =       Beneficiary.objects.get(mmap_clientid=mmap.clientid, client_cycle=mmap.client_cycle)
                beneficiary.mmapservicecentercontrolno  =   mmap.mmapservicecentercontrolno
                beneficiary.save()
            # if MultipleObjectsReturned:
            #     beneficiary.mmapservicecentercontrolno  =   mmap.mmapservicecentercontrolno
            #     beneficiary.save()
            else:
                pass

    except ObjectDoesNotExist:
        pass
        
    except MultipleObjectsReturned:
        # raise Http404("Object does not exist")
        # beneficiary.mmapservicecentercontrolno  =   mmap.mmapservicecentercontrolno
        # beneficiary.save()
        
        context =   {}
    return render(request, 'mmaptsp2/index.html', context)

def patchbenmmapid(request):
    
    mmaps=Mmap.objects.all().order_by('-id')


    try:
        for mmap in mmaps:
            if Beneficiary.objects.filter(mmap_clientid=mmap.clientid).filter(client_cycle=mmap.client_cycle).exists():
                beneficiary             =       Beneficiary.objects.get(mmap_clientid=mmap.clientid, client_cycle=mmap.client_cycle)
                beneficiary.mmapid      =       mmap.id
                beneficiary.save()
            # if MultipleObjectsReturned:
            #     beneficiary.mmapservicecentercontrolno  =   mmap.mmapservicecentercontrolno
            #     beneficiary.save()
            else:
                pass

    except ObjectDoesNotExist:
        pass
        
    except MultipleObjectsReturned:
        # raise Http404("Object does not exist")
        # beneficiary.mmapservicecentercontrolno  =   mmap.mmapservicecentercontrolno
        # beneficiary.save()
        
        context =   {}
    return render(request, 'mmaptsp2/index.html', context)

@login_required(login_url= '/users/login')
def processmmapedit(request, mmap_id):
    mmap=get_object_or_404(Mmap, pk=mmap_id)
    try:
        ben1        =  request.POST.get('ben1')
        ben2        =  request.POST.get('ben2')
        ben3        =  request.POST.get('ben3')
        ben1_dob    =  request.POST.get('ben1_dob')
        ben2_dob    =  request.POST.get('ben2_dob')
        ben3_dob    =  request.POST.get('ben3_dob')

        if ben1_dob == "":
            formatedben1_dob = None
        else:
            formatedben1_dob = datetime.strptime(ben1_dob, '%Y-%m-%d')

        if ben2_dob == "":
            formatedben2_dob = None
        else:
            formatedben2_dob = datetime.strptime(ben2_dob, '%Y-%m-%d')
             
        if ben3_dob == "":
            formatedben3_dob = None
        else:
            formatedben3_dob = datetime.strptime(ben3_dob, '%Y-%m-%d')

        ben1_rel                =  request.POST.get('ben1_rel')
        ben2_rel                =  request.POST.get('ben2_rel')
        ben3_rel                =  request.POST.get('ben3_rel')
        processed_by            =  request.POST.get('processed_by')
        processed_des           =  request.POST.get('processed_des')
        processed_date          =  request.POST.get('processed_date')
        checked_by              =  request.POST.get('checked_by')
        checked_des             =  request.POST.get('checked_des')
        checked_date            =  request.POST.get('checked_date')
        approved_by             =  request.POST.get('approved_by')
        approved_des            =  request.POST.get('approved_des')
        approved_date           =  request.POST.get('approved_date')
        recuited_by             =  request.POST.get('recuited_by')  
        branch_control_number   =  request.POST.get('branch_control_number')
        mmap_setupdate          =  request.POST.get('mmap_setupdate')  
        mmap_form_fimage        =  request.POST.get('mmap_form_fimage')
        mmap_form_bimage        =  request.POST.get('mmap_form_bimage')  
        
        
          

    except(KeyError, Mmap.DoesNotExist):
        return render(request, 'mmaptsp2/mmapdetail.html', {
            'MMAP': mmap, 'error_message': "Problem updating record",})
    else:
        mmap_update                     = Mmap.objects.get(id=mmap_id)
        ben_update                      = Beneficiary.objects.get(pk=mmap_id, client_cycle=mmap.client_cycle) 
        ben_update.ben1                 = ben1       
        ben_update.ben2                 = ben2       
        ben_update.ben3                 = ben3       
        ben_update.ben1_dob             = formatedben1_dob
        ben_update.ben2_dob             = formatedben2_dob       
        ben_update.ben3_dob             = formatedben3_dob       
        ben_update.ben1_rel             = ben1_rel       
        ben_update.ben2_rel             = ben2_rel       
        ben_update.ben3_rel             = ben3_rel   
        mmap_update.processed_by        = processed_by   
        mmap_update.processed_des       = processed_des   
        mmap_update.processed_date      = processed_date
        mmap_update.checked_by          = checked_by
        mmap_update.checked_des         = checked_des
        mmap_update.checked_date        = checked_date
        mmap_update.approved_by         = approved_by
        mmap_update.approved_by         = approved_by
        mmap_update.approved_date       = approved_date
        mmap_update.recuited_by         = recuited_by  
        mmap_update.mmap_setupdate      = mmap_setupdate  
        
        if request.FILES.get('mmap_form_fimage'):
            mmap_update.mmap_form_fimage = request.FILES.get('mmap_form_fimage')          
        if request.FILES.get('mmap_form_bimage'):
            mmap_update.mmap_form_bimage = request.FILES.get('mmap_form_bimage')

        ben_update.save()
        mmap_update.save()    
        return HttpResponseRedirect(reverse('mmaptsp2:mmapdetail', args=(mmap_id,)))
    
def exportdata (request, exporttype):    
    # cuser = request.user
    expdatestart = request.GET.get('expdatestart')    
    Fdatestart = datetime.strptime(expdatestart, '%Y-%m-%d')
    expdateend = request.GET.get('expdateend')
    Fdateend = datetime.strptime(expdateend, '%Y-%m-%d')
    #mmap = Mmap.objects.filter(mmap_setupdate__range=[Fdatestart, Fdateend]).order_by('-mmap_setupdate')
    #mmap = Mmap.objects.filter(mmap_expired__range=[Fdatestart, Fdateend]).order_by('-mmap_expired')
    filtertype = request.GET.get('filtertype')

    #if filtertype == "Expired Date":
        #mmap = Mmap.objects.filter(mmap_expired__range=[Fdatestart, Fdateend]).order_by('-mmap_expired')

    user = request.user    
    mmap_list           =       Mmap.objects.filter(expired_status="False")    
    if user.can_selectbranch==False:
        mmap_list           =       mmap_list.filter(mmap_branch=user.user_branch)  
    
    if exporttype == 'csv':

        if filtertype == 'expired-date':
            mmap = mmap_list.filter(mmap_expired__range=[Fdatestart, Fdateend]).order_by('-mmap_expired')
        elif filtertype == 'reg-date':
            mmap = mmap_list.filter(mmap_setupdate__range=[Fdatestart, Fdateend]).order_by('-mmap_setupdate')

        exportresponse = HttpResponse(content_type='text/csv')
        exportresponse['Content-Disposition'] = 'attachment; filename=Mmap' + str(datetime.now())+'.csv'    
        writer=csv.writer(exportresponse)
        writer.writerow(['Name', 'Date Registered', 'Date Expired', 'Encode Date','Client Code', 'SCCN', 'Branch', 'Premium'])
        for mmapfilter in mmap:        
            writer.writerow([mmapfilter.mmap_name, mmapfilter.mmap_setupdate, mmapfilter.mmap_expired, mmapfilter.mmap_encodedate,
                            mmapfilter.client_code, mmapfilter.mmapservicecentercontrolno, mmapfilter.mmap_branch, mmapfilter.mmap_premium])
        sumpremium = mmap.aggregate(Sum('mmap_premium'))
        writer.writerow(['', '', '', '','','', 'Total', sumpremium['mmap_premium__sum']])
        return exportresponse

    if exporttype == 'xls':
        
        #mmap = Mmap.objects.filter(mmap_expired__range=[Fdatestart, Fdateend]).order_by('-mmap_expired')
        if filtertype == 'expired-date':
            mmap = mmap_list.filter(mmap_expired__range=[Fdatestart, Fdateend]).order_by('-mmap_expired')
        elif filtertype == 'reg-date':
            mmap = mmap_list.filter(mmap_setupdate__range=[Fdatestart, Fdateend]).order_by('-mmap_setupdate')
        
        exportresponse = HttpResponse(content_type='application/ms-excel')
        exportresponse['Content-Disposition'] = 'attachment; filename=Mmap' + str(datetime.now())+'.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws=wb.add_sheet('Mmap')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Name', 'Date Registered', 'Date Expired', 'Encode Date','Client Code', 'SCCN', 'Branch', 'Premium']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)  
        #rows = Mmap.objects.filter(mmap_expired__range=[Fdatestart, Fdateend]).order_by('-mmap_expired').values_list('mmap_name',
        #        'mmap_setupdate','mmap_expired', 'mmap_encodedate', 'mmap_branch')
        rows = mmap.values_list('mmap_name','mmap_setupdate','mmap_expired', 'mmap_encodedate', 'client_code', 'mmapservicecentercontrolno', 'mmap_branch', 'mmap_premium')
        font_style = xlwt.XFStyle()
        for row in rows:
            row_num+=1
            for col_num in range(len(row)):
                if col_num == len(row)-1:
                    ws.write(row_num, col_num, int(row[col_num]), font_style)
                else:
                    ws.write(row_num, col_num, str(row[col_num]), font_style)
                #if row_num == len(rows):
            
                #    font_style.font.bold = True
                #    ws.write(row_num+1, col_num, str(coltotal[col_num]), font_style)

        font_style = xlwt.XFStyle()
        font_style.font.bold = True      
        sumpremium = mmap.aggregate(Sum('mmap_premium'))
        coltotal = ['', '', '', '','','', 'Total', sumpremium['mmap_premium__sum']]
        for col_num in range(len(coltotal)):
            ws.write(len(mmap)+1, col_num, coltotal[col_num], font_style)        
        wb.save(exportresponse)
        return exportresponse

    if exporttype == 'pdf':
        exportresponse = HttpResponse(content_type='application/pdf')
        exportresponse['Content-Disposition'] = 'inline; attachment; filename=Mmap' + str(datetime.now())+'.pdf'
        exportresponse['Content-Transfer-Encoding'] = "binary"
        _now = datetime.now()
        #rows = mmap.values_list('mmap_name','mmap_setupdate','mmap_expired', 'mmap_encodedate', 'mmap_branch', 'mmap_premium').order_by('-mmap_expired')
        #mmap = Mmap.objects.filter(mmap_expired__range=[Fdatestart, Fdateend]).order_by('-mmap_expired')
        if filtertype == 'expired-date':
            mmap = mmap_list.filter(mmap_expired__range=[Fdatestart, Fdateend]).order_by('-mmap_expired')
        elif filtertype == 'reg-date':
            mmap = mmap_list.filter(mmap_setupdate__range=[Fdatestart, Fdateend]).order_by('-mmap_setupdate')
        sumpremium = mmap.aggregate(Sum('mmap_premium'))
        context = {'page_obj': mmap, 
                    'total': sumpremium['mmap_premium__sum'], 
                    'today': _now,
                    'user': user}
        html_string = render_to_string('mmaptsp2/outputpdf.html', context)
        html=HTML(string=html_string)

        result = html.write_pdf()

        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            #output = open(output.name, 'rb')
            output.seek(0)
            exportresponse.write(output.read())
        return exportresponse



def allexpcurrentexportdata (request, exporttype):  
    user        =   request.user   
    stats       =   request.GET.get('stats')
    

    if user.can_selectbranch:
        mmap_list           =       Mmap.objects.all()
    else:
        mmap_list           =       Mmap.objects.filter(mmap_branch=user.user_branch)       
    
    if stats == 'Expired':
        mmap                =       mmap_list.filter(expired_status="True")
        # page_header         =       'MMAP Expired List'
    else:
        mmap                =       mmap_list.filter(expired_status="False")
        # page_header         =       'MMAP Current List'  



    if exporttype == 'csv':

        # if filtertype == 'expired-date':
        #     mmap = mmap_list.filter(mmap_expired__range=[Fdatestart, Fdateend]).order_by('-mmap_expired')
        # elif filtertype == 'reg-date':
        #     mmap = mmap_list.filter(mmap_setupdate__range=[Fdatestart, Fdateend]).order_by('-mmap_setupdate')

        exportresponse = HttpResponse(content_type='text/csv')
        exportresponse['Content-Disposition'] = 'attachment; filename=Mmap' + str(datetime.now())+'.csv'    
        writer=csv.writer(exportresponse)
        writer.writerow(['Name', 'Date Registered', 'Date Expired', 'Encode Date','Client Code', 'SCCN', 'Branch', 'Premium'])
        for mmapfilter in mmap:        
            writer.writerow([mmapfilter.mmap_name, mmapfilter.mmap_setupdate, mmapfilter.mmap_expired, mmapfilter.mmap_encodedate,
                            mmapfilter.client_code, mmapfilter.mmapservicecentercontrolno, mmapfilter.mmap_branch, mmapfilter.mmap_premium])
        sumpremium = mmap.aggregate(Sum('mmap_premium'))
        writer.writerow(['', '', '', '','','', 'Total', sumpremium['mmap_premium__sum']])
        return exportresponse

    if exporttype == 'xls':
        
        #mmap = Mmap.objects.filter(mmap_expired__range=[Fdatestart, Fdateend]).order_by('-mmap_expired')
        # if filtertype == 'expired-date':
        #     mmap = mmap_list.filter(mmap_expired__range=[Fdatestart, Fdateend]).order_by('-mmap_expired')
        # elif filtertype == 'reg-date':
        #     mmap = mmap_list.filter(mmap_setupdate__range=[Fdatestart, Fdateend]).order_by('-mmap_setupdate')
        
        exportresponse = HttpResponse(content_type='application/ms-excel')
        exportresponse['Content-Disposition'] = 'attachment; filename=Mmap' + str(datetime.now())+'.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws=wb.add_sheet('Mmap')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Name', 'Date Registered', 'Date Expired', 'Encode Date','Client Code', 'SCCN', 'Branch', 'Premium']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)  
        #rows = Mmap.objects.filter(mmap_expired__range=[Fdatestart, Fdateend]).order_by('-mmap_expired').values_list('mmap_name',
        #        'mmap_setupdate','mmap_expired', 'mmap_encodedate', 'mmap_branch')
        rows = mmap.values_list('mmap_name','mmap_setupdate','mmap_expired', 'mmap_encodedate', 'client_code', 'mmapservicecentercontrolno', 'mmap_branch', 'mmap_premium')
        font_style = xlwt.XFStyle()
        for row in rows:
            row_num+=1
            for col_num in range(len(row)):
                if col_num == len(row)-1:
                    ws.write(row_num, col_num, int(row[col_num]), font_style)
                else:
                    ws.write(row_num, col_num, str(row[col_num]), font_style)
                #if row_num == len(rows):
            
                #    font_style.font.bold = True
                #    ws.write(row_num+1, col_num, str(coltotal[col_num]), font_style)

        font_style = xlwt.XFStyle()
        font_style.font.bold = True      
        sumpremium = mmap.aggregate(Sum('mmap_premium'))
        coltotal = ['', '', '', '','','', 'Total', sumpremium['mmap_premium__sum']]
        for col_num in range(len(coltotal)):
            ws.write(len(mmap)+1, col_num, coltotal[col_num], font_style)        
        wb.save(exportresponse)
        return exportresponse

    if exporttype == 'pdf':
        exportresponse = HttpResponse(content_type='application/pdf')
        exportresponse['Content-Disposition'] = 'inline; attachment; filename=Mmap' + str(datetime.now())+'.pdf'
        exportresponse['Content-Transfer-Encoding'] = "binary"
        _now = datetime.now()
        #rows = mmap.values_list('mmap_name','mmap_setupdate','mmap_expired', 'mmap_encodedate', 'mmap_branch', 'mmap_premium').order_by('-mmap_expired')
        #mmap = Mmap.objects.filter(mmap_expired__range=[Fdatestart, Fdateend]).order_by('-mmap_expired')
        # if filtertype == 'expired-date':
        #     mmap = mmap_list.filter(mmap_expired__range=[Fdatestart, Fdateend]).order_by('-mmap_expired')
        # elif filtertype == 'reg-date':
        #     mmap = mmap_list.filter(mmap_setupdate__range=[Fdatestart, Fdateend]).order_by('-mmap_setupdate')
        sumpremium = mmap.aggregate(Sum('mmap_premium'))
        context = {'page_obj': mmap, 
                    'total': sumpremium['mmap_premium__sum'], 
                    'today': _now,
                    'user': user}
        html_string = render_to_string('mmaptsp2/outputpdf.html', context)
        html=HTML(string=html_string)

        result = html.write_pdf()

        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            #output = open(output.name, 'rb')
            output.seek(0)
            exportresponse.write(output.read())
        return exportresponse

@permission_required('admin.can_add_log_entry')
def csv_upload(request):
    pagelink = 'mmaptsp2/csv_upload.html'

    prompt = {
        'order': 'Order of csv to be uploaded LNAME, FNAME, Membership Date, Date of Birth, Branch'
    }

    if request.method == "GET":
        return render(request, pagelink, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file')

    # data_set = csv_file.read().decode('UTF-8')
    data_set = csv_file.read().decode('ISO-8859-1')
    io_string = io.StringIO(data_set)
    next(io_string)

    for column in csv.reader(io_string, delimiter=',', quotechar="|"):

        client_branch               =       column[4]
        reg_date                    =       datetime.strptime(column[2], '%Y-%m-%d')
        client_dob                  =       datetime.strptime(column[3], '%Y-%m-%d')
        getclientcodes              =       Clientaccountcode.objects.get(branch=client_branch)
        client_zipcode              =       getclientcodes.zipcode
        client_branchcode           =       getclientcodes.branchcode
    

        getbranchcount = Client.objects.filter(client_branchcode=client_branchcode)
        
        branchcodecounts =  1

        if getbranchcount:
            for getcounts in getbranchcount:
                branchcodecounts+=1   

        client_code         =           str(client_branchcode) + str(client_zipcode) + str(branchcodecounts)
        
        
        # reg_date = request.POST.get('reg_date')   

        if request.FILES.get('client_image'):
            client_image = request.FILES.get('client_image')
        else:
            client_image='profile_pic/default_image.png'

        
        
        _, client = Client.objects.update_or_create(

                client_fname        =       column[1],
                client_lname        =       column[0],
                reg_date            =       reg_date,
                client_code         =       client_code,
                client_branch       =       client_branch,
                client_branchcode   =       client_branchcode,
                client_zipcode      =       client_zipcode,
                client_dob          =       client_dob
            )
            
        
        


            


        clientname                  =   column[0] + ", " + column[1]
        getbranchcode               =   Branchcode.objects.get(bname=client_branch)
        branchcode                  =   getbranchcode.bcode
        getbranchcodecount          =   Sccn.objects.filter(sccnbcode=branchcode)
        branchcodecounts            =   1
        zeros                       =  "0"
        

        if getbranchcodecount:
            for getcounts in getbranchcodecount:
                branchcodecounts+=1   

        if branchcodecounts <= 9:
            zeros = "0000"
        
        elif branchcodecounts <= 99:
            zeros = "000"

        elif branchcodecounts <= 999:
            zeros = "00"
    
        elif branchcodecounts <= 9999:
            zeros = "0"
        
        else:
            zeros = ''

        sscnservicecentercontrolno         =           str(branchcode) + str(zeros) + str(branchcodecounts)

        client_tablecount           =   Client.objects.count()
        client                      =   Client.objects.get(pk=client_tablecount)
        client_cycle                =   int(client.client_cycle) + 1
        clientid                    =   client.id
        client_code                 =   client.client_code
        clientimg                   =   client.client_image
        # clientid                    =   clientid
        clientimg                   =   clientimg
        client_code                 =   client_code
        mmap_dob                    =   client.client_dob
        mmap_age                    =   int((datetime.now().date() - client.client_dob).days / 365.25)
        
        
        mmap_sex                    =   client.client_gender
        # client_cycle                =   int(client.client_cycle) + 1
        client.client_cycle         =   client_cycle   
        client.save()     
        # d_o_b                       =   int((datetime.now().date() - client.client_dob).days / 365.25)
        mmaptype                    =   ""
        mmap_premium                =   0

        if (mmap_age <= 17):
            mmaptype            = "N/A"
            
        
        elif (mmap_age <= 65):
            mmaptype            = "18-64"
            mmap_premium        =  900

        elif (mmap_age <= 70):
            mmaptype = "65-69"
            mmap_premium        =  850
        
        elif mmap_age <=120 :
            mmaptype = "70-Up"
            mmap_premium        =  800
        
        
        mmap_setupdate                  =   datetime.strptime(column[2], '%Y-%m-%d')
        mmap_name                       =   client.client_lname + ", " + client.client_fname + " " + client.client_mname
        mmap_branch                     =   client.client_branch
        mmap_expired                    =   datetime (mmap_setupdate.year + 1, mmap_setupdate.month, mmap_setupdate.day)
            
        _, created = Mmap.objects.update_or_create(
            
            mmap_name                       =   mmap_name,
            mmap_sex                        =   mmap_sex,
            mmap_age                        =   mmap_age,
            mmap_setupdate                  =   mmap_setupdate,
            mmap_expired                    =   mmap_expired,
            mmap_dob                        =   mmap_dob,
            mmap_branch                     =   mmap_branch,
            mmapbcode                       =   branchcode,
            mmapservicecentercontrolno      =   sscnservicecentercontrolno,
            clientid                        =   clientid,
            client_code                     =   client_code,
            clientimg                       =   clientimg,
            mmap_type                       =   mmaptype,
            client_cycle                    =   client_cycle,
            mmap_premium                    =   mmap_premium                           

        )

        _, sscn = Sccn.objects.update_or_create(
                sscnservicecentercontrolno      =       sscnservicecentercontrolno,                                 
                sccnbcode                       =       branchcode, 
                sccnbranch                      =       mmap_branch, 
                client_name                     =       mmap_name,
                mmap_setupdate                  =       mmap_setupdate,
                mmap_expired                    =       mmap_expired
            )
        # clientname = column[1] + " " + column[0]
        # created = Mmap.objects.update_or_create(
            
        #     mmap_name       =   clientname,
        #     mmap_setupdate  =   column[2],  
        #     dob             =   column[3],
        #     branch          =   column[4]

        # )
        # created.save()
        _, beneficiary = Beneficiary.objects.update_or_create(
                mmapid                          =       sscnservicecentercontrolno,                                 
                ben_mmap_name                   =       clientname, 
                mmap_clientid                   =       clientid, 
                client_cycle                    =       client_cycle
            )

    context={}

    return render(request, pagelink, context)

def newrenewstatus(request):
    # unrenewlistJSON = []
    unrenewlist = {}
    user        =   request.user  
    clients     =   Client.objects.all()

    # mmaps       =   Mmap.objects.filter(expired_status=False)


    if user.can_selectbranch==False:
        clients =   clients.filter(client_branch=user.user_branch).filter(client_isdisabled=False)
        
    for client in clients:
        try:
            if Mmap.objects.filter(expired_status=False).filter(clientid=client.id).exists():
                pass
            else:

            # if Mmap.objects.filter(expired_status=False).filter(clientid=client.id).count() == 0:
                # unrenewlist[client.id]=client.client_fname + " " + client.client_mname + " " + client.client_lname
                unrenewlist[client.id] = {'clientID': client.id, 'clientBranch':client.client_branch, 
                    'clientName': client.client_fname + " " + client.client_mname + " " + client.client_lname,
                    'clientCycle':client.client_cycle, 'clientCelnumber': client.client_celnumber}

        except Mmap.DoesNotExist:  
            pass              
            # unrenewlist[client.id]=client.client_fname + " " + client.client_mname + " " + client.client_lname

        except MultipleObjectsReturned:
            pass
        unrenewlistCount     = len(unrenewlist)
        clientCount = clients.count()
    return render(request, 'mmaptsp2/newrenewstatus.html', 
            {'page_obj': unrenewlist, 
            'unrenewlistCount':unrenewlistCount,
            'clientCount':clientCount})


    


