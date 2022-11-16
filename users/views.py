from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import User, Comment
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, logout, login
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from clients.models import Branch, Client
from mmaptsp2.models import Mmap, Beneficiary
from datetime import datetime, timedelta

# from .forms import CreateUserForm

# def userreg(request):
#     form        =       CreateUserForm()
#     if request.method   ==   'POST':
#         form    =       CreateUserForm(request.POST)
#         if form.is_valid():
#             form.save()

#     context     =       {'form': form}
#     return render(request, 'users/userreg.html', context)


@login_required(login_url= '/users/login')
def index(request):
    #user_list = User.objects.order_by('-id')[:5]
    #context = {'user_list': user_list}
    #return render(request, 'users/index.html', context)
    datetoday = datetime.now().date()
    #expiration validation
    expiration_validation   =   Mmap.objects.filter(expired_status="False")
    # exp_count               =   expiration_validation.count()
    user = request.user
       


    for clientexp   in expiration_validation:
        if clientexp.mmap_expired < datetoday:
            update_expired  =   get_object_or_404(Mmap, pk=clientexp.id)
            update_expired.expired_status  =   "True"
            update_expired.save()
        

    
    user_list       =       User.objects.all().order_by('-id')

    if user.can_selectbranch==False:
        user_list = User.objects.filter(user_branch=user.user_branch)


    paginator       =       Paginator(user_list, 5)    
    page_number     =       request.GET.get('page')
    user_list       =       paginator.get_page(page_number)

    datenow         =       datetime.now().date()
    fdatenow        =       datenow.strftime("%Y-%m-%d") 
    days30          =       datenow + timedelta(days=30)
    fdays30         =       days30.strftime("%Y-%m-%d") 
    mmapraw         =       Mmap.objects.filter(mmap_expired__range=[fdatenow, fdays30]).order_by('mmap_expired')
    mmap            =       mmapraw.filter(expired_status="False")
    # mmapfilter = mmap.filter(mmap_branch='Lutopan')
    
    if user.can_selectbranch==False:
        mmap = mmap.filter(mmap_branch=user.user_branch)

    context = {'page_obj': user_list, 'mmap': mmap, 'datenow': fdatenow, 'days30' : fdays30}    

    return render (request, 'users/index.html', context)

@login_required(login_url= '/users/login')
def search(request):
    term = request.GET.get('search', '')
    user_list = User.objects.filter(Q(user_fname__icontains=term) | Q(user_lname__icontains=term)).order_by('-id')
    paginator = Paginator(user_list, 5)    
    page_number = request.GET.get('page')
    user_list = paginator.get_page(page_number)
    return render (request, 'users/index.html', {'page_obj': user_list})

@login_required(login_url= '/users/login')
def add(request):
    branches = Branch.objects.only('branches')
    context = {'branches': branches}
    return render(request, 'users/add.html', context)

@login_required(login_url= '/users/login')
def processadd(request):
    user_name = request.POST.get('user_name')
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    email = request.POST.get('email')
    user_branch = request.POST.get('user_branch')
    position = request.POST.get('position')
    
    if request.FILES.get('image'):
        user_pic = request.FILES.get('image')
    else:
        user_pic='profile_pic/default_image.jpg'

    try:

        m=User.objects.get(user_name=user_name)
        #if username already exist
        return render(request, 'users/add.html', { 
            'error_message': "Username already exist: " + user_name, 'fname': fname, 'lname': lname, 'email':email, 'position': position,
                        'user_name': user_name, 'user_branch': user_branch
            })

        n=User.objects.get(user_email=email)
        #if email already exist
        return render(request, 'users/add.html', { 
            'error_message': "Duplicated Email: " + email, 'fname': fname, 'lname': lname, 'email':email, 'position': position,
                        'user_name': user_name, 'user_branch': user_branch
            })

    except ObjectDoesNotExist:
        user=User.objects.create(user_email=email, user_name=user_name, user_fname=fname,
        user_lname=lname, user_branch=user_branch, user_position=position, user_image=user_pic)
        user.save()
        return HttpResponseRedirect('/users')

@login_required(login_url= '/users/login')        
def detail(request, profile_id):
    try:
        user = User.objects.get(pk=profile_id)
        comments = Comment.objects.filter(user_id=profile_id)
        comments_count = Comment.objects.filter(user_id=profile_id).count()
        context = {'users': user, 
                    'comments': comments, 'comments_count': comments_count}
    except User.DoesNotExist:
        raise Http404("Profile does not exist")
    return render(request, 'users/detail.html', context)

@login_required(login_url= '/users/login')
def addcomment(request):
    comment_text = request.POST.get('comment')
    user_id = request.POST.get('user_id')
    name = request.POST.get('name')
    email = request.POST.get('email')

    comment = Comment.objects.create(user_id=user_id, body=comment_text, name=name, email=email)
    comment.save()
    return HttpResponseRedirect(reverse('users:detail', args=(user_id,)))
@login_required(login_url= '/users/login')
def delete(request, profile_id):
    User.objects.filter(id=profile_id).delete()
    return HttpResponseRedirect('/users')

@login_required(login_url= '/users/login')
@permission_required('users.change_user', login_url= '/users/login')
def edit(request, profile_id):
    try:
        user = User.objects.get(pk=profile_id)
        branches = Branch.objects.only('branches') 
    except User.DoesNotExist:
        raise Http404("Profile does not exist")
    return render(request, 'users/edit.html', {'users': user, 'branches': branches})

@login_required(login_url= '/users/login')
def processedit(request, profile_id):
    user=get_object_or_404(User, pk=profile_id)
    profile_pic=request.FILES.get('image')
    try:
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        position = request.POST.get('position')
        user_branch = request.POST.get('user_branch')
    except(KeyError, User.DoesNotExist):
        return render(request, 'users/detail.html', {
            'user': user,
            'error_message': "Problem updating record",
        })
    else:
        user_profile = User.objects.get(id=profile_id)
        user_profile.user_fname=fname
        user_profile.user_lname=lname
        user_profile.user_email=email
        user_profile.user_branch=user_branch
        user_profile.user_position=position
        if profile_pic:
            user_profile.user_image=profile_pic
        user_profile.save()
        return HttpResponseRedirect(reverse('users:detail', args=(profile_id,)))

def loginview(request):
    return render(request, 'users/login.html')


def process(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    user = authenticate(username=username, password=password )
    if user is not None:
        login(request, user)
        
        return HttpResponseRedirect('/users')
        # return redirect('users:daysindex')
        # datenow = datetime.now()
        # days30 = datenow + timedelta(days=30)
        # mmap = Mmap.objects.filter(mmap_expired__range=[datenow, days30]).order_by('-mmap_expired')
        # users= User.objects.all().order_by('-id')

        # return render (request, '/users/index.html', {'mmap': mmap, 'datenow': datenow, 'days30':days30, 'page_obj': users })
    
    else:
        return render(request, 'users/login.html', {
            'error_message': "Login Failed"
        })

def processlogout(request):
    logout(request)
    return HttpResponseRedirect('/users/login')

# def daysindex(request, profile_id):
#     datenow = datetime.now()
#     days30 = datenow + timedelta(days=30)
#     mmap = Mmap.objects.filter(mmap_expired__range=[datenow, days30]).order_by('-mmap_expired')

#     return render (request, 'users/index2.html', {'mmap': mmap})

