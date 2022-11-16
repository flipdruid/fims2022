from django import forms

from .models import Event, Event_type
from datetime import datetime

date_time_now = datetime.now()

class EventForm(forms.ModelForm):
    get_event_type  = Event_type.objects.values_list('event_type_name', flat=True)
    
    event_type = forms.ModelChoiceField(queryset=get_event_type, empty_label=None, 
                                        widget=forms.Select(attrs={'class': 'form-control', 'id': 'event_type', 'required' : True}))
                    

    class Meta:
        model       = Event
        fields      = ['event_name', 'event_type', 'event_date', 'event_time']
        widgets     = {
            'event_name' : forms.TextInput(attrs={'class': 'form-control', 'id': 'event_name', "required": True}),
            'event_date' : forms.DateInput(
                
                format=('%Y-%m-%d'), # this format for display current date to input type date
                attrs={'class': 'form-control', 
                       'placeholder': 'Select a date',
                       'type': 'date',
                    #    'value' :date_time_now,
                    #    'initial' : date_time_now.strftime('%m/%d/%Y'),
                    #    'initial' : date_time_now.strftime('%Y-%m-%d'), # this format for display current date to input type date
                       'id': 'event_date',
                       'required': True
                         # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                      }),
            'event_time' : forms.TimeInput(
            format=('%H:%M'),
            attrs={'class': 'form-control', 
                    'placeholder': 'Select a time',
                    'type': 'time',
                    'id': 'event_time',
                    'required': True
                        # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                    })
            # 'event_date' : forms.EmailInput(attrs={'class': 'form-control', 'id': 'event_date'}),
            # 'course': forms.TextInput(attrs={'class': 'form-control', 'id': 'event_setupDate'})

        }