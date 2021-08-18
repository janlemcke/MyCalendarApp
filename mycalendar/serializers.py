from rest_framework import serializers
from mycalendar.models import Calendar, Event,RecurrentEvent


class CalendarSerializer(serializers.ModelSerializer):
    visible_for = serializers.SerializerMethodField("get_visible_for")
    editable_by = serializers.SerializerMethodField("get_editable_by")

    def get_visible_for(self, obj):
        return "; ".join(obj.visible_for.all().values_list('email', flat=True))

    def get_editable_by(self, obj):
        return "; ".join(obj.editable_by.all().values_list('email', flat=True))

    class Meta:
        model = Calendar
        exclude = ("owner",)

class RecurrentEventSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField("get_title")
    rrule = serializers.SerializerMethodField("get_rrule")
    icon = serializers.SerializerMethodField("get_icon")

    def get_title(self, obj):
        return obj.name

    def get_rrule(self, obj):
        rrule = {}
        rrule["freq"] = "weekly"
        rrule["interval"] = 3
        rrule["dtstart"] = obj.start_date
        rrule["until"] = "2021-10-18"
        return rrule

    def get_icon(self, obj):
        if obj.event_type == "AR":
            return "briefcase"
        else:
            return "tree"

    class Meta:
        model = RecurrentEvent
        fields = ("title","rrule","icon","event_id","event_type")

class EventSerializer(serializers.ModelSerializer):

    title  = serializers.SerializerMethodField("get_title")
    start = serializers.SerializerMethodField("get_start")
    end = serializers.SerializerMethodField("get_end")
    icon = serializers.SerializerMethodField("get_icon")

    def get_icon(self, obj):
        if obj.event_type == "AR":
            return "briefcase"
        else:
            return "tree"

    def get_title(self, obj):
        return obj.name

    def get_start(self,obj):
        return obj.start_date

    def get_end(self,obj):
        return obj.end_date

    class Meta:
        model = Event
        fields = ("title","start","end","icon","event_id","event_type")
