from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from mycalendar.forms import CalendarForm, CalendarEditForm
from mycalendar.models import Calendar, Event

@login_required
def homeView(request):
    context = {}

    if request.POST:
        if request.POST['action'] == 'create':
            form = CalendarForm(request.POST)
            if form.is_valid():
                calendar = form.save(commit=False)
                calendar.owner_id = request.user.pk
                calendar.save()

        if request.POST['action'] == 'edit':
            form = CalendarEditForm(request.POST)
            if form.is_valid():
                calendar = form.save(commit=False)
                calendar.owner_id = request.user.pk
                calendar.save()

    calendars = Calendar.objects.filter(owner=request.user)

    createform = CalendarForm()
    editform = CalendarEditForm(initial={"user_id": request.user.pk})
    context["createform"] = createform
    context["editform"] = editform

    return render(request, "home.html", context)