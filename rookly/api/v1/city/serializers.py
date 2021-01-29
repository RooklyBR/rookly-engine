from rest_framework import serializers

from rookly.common.models import State, City


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ["id", "slug", "name", "city"]
        ref_name = None

    city = serializers.SerializerMethodField()

    def get_city(self, obj):
        return obj.states.all().values("id", "name")


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name", "state"]
        ref_name = None

    state = StateSerializer(many=False)
