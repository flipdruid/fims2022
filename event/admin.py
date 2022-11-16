from django.contrib import admin

# Register your models here.

from .models import Event_type, Event, Event_positions, Candidates, Voter, Key_var


@admin.register(Event_type)
class Event_typeAdmin(admin.ModelAdmin):
    list_display = ['id', 'event_type_name','event_description']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'event_name','event_type','event_date','event_time', 'event_setupDate', 'user_name','user_id']

@admin.register(Key_var)
class Key_varAdmin(admin.ModelAdmin):
    list_display = ['id', 'eventid','eventcaption']