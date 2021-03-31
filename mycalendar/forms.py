# -*- coding: utf-8 -*-
from django import forms
from mycalendar.models import Calendar, Event
from account.models import Account


class CalendarForm(forms.ModelForm):
    visible_for = forms.CharField()
    editable_by = forms.CharField()

    class Meta:
        model = Calendar
        exclude = ("owner", "visible_for", "editable_by")

    def save(self, commit=True):
        calendar = self.instance
        for email in self.cleaned_data["visible_for"].split(";"):
            if Account.objects.filter(email=email).exists():
                calendar.visible_for.add(email)
        for email in self.cleaned_data["editable_by"].split(";"):
            if Account.objects.filter(email=email).exists():
                calendar.editable_by.add(email)
        if commit:
            calendar.save()
        return calendar


def get_calendars(user_id):
    calendars = Calendar.objects.filter(owner=user_id)
    print(calendars)
    choices = []

    for calendar in calendars:
        choices.append((calendar.pk, calendar.name))

    return choices


class CalendarEditForm(CalendarForm):

    def __init__(self, *args, **kwargs):
        super(CalendarEditForm, self).__init__(*args, **kwargs)
        self.fields["calendars"] = forms.ChoiceField(choices=get_calendars(self.initial["user_id"]), required=True)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ()
