from rest_framework import serializers

# My Stuff
from gateway.models import Router


class RouterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Router
        fields = '__all__'

