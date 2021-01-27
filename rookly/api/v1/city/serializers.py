from rest_framework import serializers

from rookly.authentication.models import State, City


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ["id", "slug", "name"]
        ref_name = None


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name", "state"]
        ref_name = None

    state = StateSerializer(many=False)
