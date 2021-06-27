from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from mycalendar.forms import CalendarForm, CalendarEditForm
from mycalendar.models import Calendar
from mycalendar.serializers import CalendarSerializer


@login_required
def homeView(request):
    context = {}

    if request.POST:
        if request.POST['action'] == 'create':
            form = CalendarForm(request.POST)
            if form.is_valid():
                form.set_owner(request.user)
                form.save()

        if request.POST['action'] == 'edit':
            form = CalendarEditForm(request.POST)
            if form.is_valid():
                form.save(commit=True)

        if request.POST['action'] == 'delete':
            calendar = Calendar.objects.get(calendar_id=request.POST["calendar_id"])
            if calendar.owner == request.user:
                calendar.delete()

    queryset = Calendar.objects.filter(owner=request.user.pk)
    context["calendars"] = CalendarSerializer(queryset, many=True).data

    context["createform"] = CalendarForm()
    context["editform"] = CalendarEditForm(initial={"user_id": request.user.pk, "owner": request.user})

    context["my_calendars"] = queryset

    return render(request, "home.html", context)
