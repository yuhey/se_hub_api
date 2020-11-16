from rest_framework import serializers
from api.models.bp import Bp


class BpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bp
        fields = ('group1_id', 'group2_id')
