# -*- coding: utf-8 -*-
from django import forms
from mycalendar.models import Calendar, Event
from account.models import Account

class CalendarForm(forms.ModelForm):
    visible_for = forms.CharField()
    editable_by = forms.CharField()

    class Meta:
        model = Calendar
        exclude = ("owner","visible_for","editable_by")

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

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ()