from rest_framework import serializers
from . models import inputs

class inputsSerializers(serializers.ModelSerializer):
    class Meta:
        model = inputs
        fields = '__all__'
