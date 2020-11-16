from rest_framework import serializers
from api.models.data import Data


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ('title', 'file')
