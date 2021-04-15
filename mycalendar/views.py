from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from mycalendar.forms import CalendarForm
from mycalendar.models import Calendar, Event

@login_required
def homeView(request):
    context = {}

    if request.POST:
        form = CalendarForm(request.POST)
        if form.is_valid():
            calendar = form.save(commit=False)
            calendar.owner_id = request.user.pk
            calendar.save()
            print(calendar)

    form = CalendarForm()
    context["form"] = form

    return render(request, "home.html", context)