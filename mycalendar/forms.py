# -*- coding: utf-8 -*-
from django import forms
from mycalendar.models import Calendar, Event, RecurrentEvent
from account.models import Account
from django.db.models import Q


class CalendarForm(forms.ModelForm):
    visible_for = forms.CharField(required=False)
    editable_by = forms.CharField(required=False)

    class Meta:
        model = Calendar
        exclude = ("owner", "visible_for", "editable_by")

    def set_owner(self, user):
        calendar = self.instance
        calendar.owner_id = user.pk
        self.instance = calendar

    def save(self, commit=True):
        calendar = self.instance

        calendar.save()

        for email in self.cleaned_data["visible_for"].split(";"):
            if Account.objects.filter(email=email).exists():
                user = Account.objects.filter(email=email).get()
                calendar.visible_for.add(user.pk)
        for email in self.cleaned_data["editable_by"].split(";"):
            if Account.objects.filter(email=email).exists():
                user = Account.objects.filter(email=email).get()
                calendar.editable_by.add(user.pk)

        if commit:
            calendar.save()

        return calendar


def get_calendars(user_id):
    calendars = Calendar.objects.filter(Q(owner=user_id) | Q(editable_by=user_id))
    choices = []

    for calendar in calendars:
        choices.append((calendar.pk, calendar.name))

    return choices


class CalendarEditForm(CalendarForm):
    visible_for = forms.CharField(required=False)
    editable_by = forms.CharField(required=False)
    calendar_id = forms.CharField(required=True)

    class Meta:
        model = Calendar
        exclude = ("visible_for", "editable_by",)

    def __init__(self, *args, **kwargs):
        super(CalendarEditForm, self).__init__(*args, **kwargs)
        if self.initial:
            self.fields["calendars"] = forms.ChoiceField(choices=get_calendars(self.initial["user_id"]), required=True)

    def save(self, commit=True):
        calendar = Calendar.objects.get(calendar_id=self.cleaned_data["calendar_id"])
        calendar.name = self.cleaned_data["name"]
        calendar.editable_by.clear()
        calendar.visible_for.clear()

        for email in self.cleaned_data["visible_for"].split(";"):
            if Account.objects.filter(email=email).exists():
                user = Account.objects.filter(email=email).get()
                calendar.visible_for.add(user.pk)

        for email in self.cleaned_data["editable_by"].split(";"):
            if Account.objects.filter(email=email).exists():
                user = Account.objects.filter(email=email).get()
                calendar.editable_by.add(user.pk)

        if commit:
            calendar.save()

        return calendar


class EventCreateForm(forms.ModelForm):
    start_date = forms.DateTimeField(input_formats=["%d.%m.%Y %H:%M"], required=True)
    end_date = forms.DateTimeField(input_formats=["%d.%m.%Y %H:%M"], required=False)

    def set_calendar(self, calendar_id):
        event = self.instance
        event.calendar_id = calendar_id
        self.instance = event

    class Meta:
        model = Event
        exclude = ('calendar',)


class EventEditForm(forms.ModelForm):
    start_date = forms.DateTimeField(input_formats=["%d.%m.%Y %H:%M"], required=True)
    end_date = forms.DateTimeField(input_formats=["%d.%m.%Y %H:%M"], required=False)
    event_id = forms.CharField(required=True)

    def save(self, commit=True):
        event = Event.objects.get(event_id=self.cleaned_data["event_id"])
        event.name = self.cleaned_data["name"]
        event.start_date = self.cleaned_data["start_date"]
        event.end_date = self.cleaned_data["end_date"]
        event.event_type = self.cleaned_data["event_type"]
        if commit:
            event.save()

        return event

    class Meta:
        model = Event
        exclude = ("calendar",)


class RecurrentEventCreateForm(EventCreateForm):
    start_date = None
    end_date = None

    frequence = forms.ChoiceField(label="Frequenz", choices=RecurrentEvent.FREQ_CHOICES, required=False)
    interval = forms.IntegerField(label="Intervall", min_value=0, required=False)

    class Meta:
        model = RecurrentEvent
        fields = ("frequence", "interval")
