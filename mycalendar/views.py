from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from mycalendar.forms import CalendarForm, CalendarEditForm, EventCreateForm, EventEditForm
from mycalendar.models import Calendar
from mycalendar.serializers import CalendarSerializer, EventSerializer, RecurrentEventSerializer
from django.db.models import Q


def getEventsForCalender(selected_calendar):
    calendar = Calendar.objects.get(calendar_id=selected_calendar)
    serializedEvents = RecurrentEventSerializer(calendar.event_set.all(), many=True).data
    return serializedEvents


@login_required
def homeView(request):
    context = {}
    createEventForm = EventCreateForm()
    editEventForm = EventEditForm()

    # Events stuff
    if "selected_calendar" in request.GET:
        selected_calendar = request.GET["selected_calendar"]
        firstCalendar = True
    else:
        firstCalendar = Calendar.objects.filter(Q(owner=request.user.pk) | Q(visible_for=request.user)).first()
        if firstCalendar:
            selected_calendar = firstCalendar.calendar_id

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
                firstCalendar = Calendar.objects.filter(Q(owner=request.user.pk) | Q(visible_for=request.user)).first()
                if firstCalendar:
                    selected_calendar = firstCalendar.calendar_id

        if request.POST['action'] == "create_event":
            form = EventCreateForm(request.POST)
            if form.is_valid():
                form.set_calendar(selected_calendar)
                form.save()
                createEventForm = EventCreateForm()
            else:
                createEventForm = form

        if request.POST['action'] == "edit_event":
            form = EventEditForm(request.POST)
            if form.is_valid():
                form.save()
                editEventForm = EventEditForm()
            else:
                editEventForm = form

    # calendar stuff
    queryset_visible = Calendar.objects.filter(Q(owner=request.user.pk) | Q(visible_for=request.user))
    queryset_editable = Calendar.objects.filter(Q(owner=request.user.pk) | Q(editable_by=request.user))
    context["calendars"] = CalendarSerializer(queryset_editable, many=True).data

    context["createform"] = CalendarForm()
    context["editform"] = CalendarEditForm(initial={"user_id": request.user.pk, "owner": request.user})
    context["my_calendars"] = queryset_visible

    if firstCalendar:
        context["events"] = getEventsForCalender(selected_calendar)
        context["selected_calendar"] = int(selected_calendar)
    context["event_createform"] = createEventForm
    context["event_editform"] = editEventForm

    return render(request, "home.html", context)
