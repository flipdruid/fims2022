from django.shortcuts import render
from .forms import EventForm
from .models import Event, Event_type, Key_var, Event_positions
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@login_required(login_url= '/users/login')
def index (request):
    form                =   EventForm()
    events              =   Event.objects.values()
    eventLists          =   list(events)
    current_date        =   datetime.now()
    context             =   {'form': form, 'eventLists': eventLists, 'current_date': current_date}
    return render(request, 'event/index.html', context)

@csrf_exempt
@login_required(login_url= '/users/login')
def saveditevent (request):
    user = request.user
    if request.method   ==  'POST':
        event_form         =   EventForm(request.POST)
        
        sid                =   request.POST.get('eventpid')
        event_name         =   request.POST['event_name']
        event_type         =   request.POST['event_type']
        event_date         =   request.POST['event_date']
        event_time         =   request.POST['event_time']
        user_id            =   request.POST['user_id']
        user_name          =   request.POST['user_name']

        event_dateFormat   =    datetime.strptime(event_date, '%Y-%m-%d')
        # event_timeFormat   =    datetime.strptime(event_time, '%H:%M')

        if (sid==""):
            eventFormSave       =   Event(event_name=event_name,
                                        event_type=event_type, 
                                        event_date=event_dateFormat,
                                        event_time=event_time,
                                        user_id=user_id,
                                        user_name=user_name)
        else:        
            eventFormSave       =   Event(id=sid,
                                        event_name=event_name,
                                        event_type=event_type, 
                                        event_date=event_dateFormat,
                                        event_time=event_time,
                                        )

        eventFormSave.save()

        new_event_data  =   Event.objects.values()
        event_data      =   list(new_event_data)
        return JsonResponse ({'event_data': event_data})

@csrf_exempt      
@login_required(login_url= '/users/login')
def delete (request):  
    if request.method   ==  'POST':
        id = request.POST.get('sid')
        event = Event.objects.get(pk=id)
        event.delete()
        return JsonResponse({'status' : 1})
    else:
        return JsonResponse({'status' : 0})

@csrf_exempt      
@login_required(login_url= '/users/login')
def edit (request):  
    if request.method   ==  'POST':
        id      = request.POST.get('sid')
        event   = Event.objects.get(pk=id)

        event_data  =   {
            'id'                : event.id,
            'event_name'        : event.event_name,
            'event_type'        : event.event_type,
            'event_date'        : event.event_date,
            'event_time'        : event.event_time,
            'event_setupDate'   : event.event_setupDate

        }
        return JsonResponse (event_data)


@csrf_exempt      
@login_required(login_url= '/users/login')
def eventpage (request, eid):    
    event   = Event.objects.get(pk=eid)
    
    return render(request, 'event/eventsetup.html', {'event': event})


@csrf_exempt      
@login_required(login_url= '/users/login')
def eventpagejq (request):
    if request.method   ==  'POST':
        id      = request.POST.get('eid')
        # event   = Event.objects.get(pk=id)  
        eventid = Key_var.objects.get(eventcaption="Event")  
        eventid.eventid = id
        eventid.save()
        return JsonResponse ({'status' : 1, 'evid': id})
    else:
        return JsonResponse ({'status' : 0})

@csrf_exempt      
@login_required(login_url= '/users/login')
def eventpagesetup (request): 
    getevent    = Key_var.objects.get(eventcaption="Event") 
    eventid     = getevent.eventid
    event       = Event.objects.get(pk=eventid)

    return render(request, 'event/eventsetup.html', {'event': event})

@csrf_exempt      
@login_required(login_url= '/users/login')
def saveditpos (request): 
    if request.method   ==  'POST':
        sid             =   request.POST.get('posid')
        eventId         = request.POST.get('eventId')
        PosName         = request.POST.get('PosName')
        PosVac          = request.POST.get('PosVac')
        NewPosition     = request.POST.get('NewPosition')

        if NewPosition:
            positions     =   Event_positions(eventid=eventId,
                                    position=PosName, 
                                    avail_seats=PosVac)

        
        positions.save()

        new_event_data  =   Event_positions.objects.values()
        pos_data        =   list(new_event_data)

        return JsonResponse ({'pos_data': pos_data})

        
                                    
        


