from rest_framework import serializers
from api.models.data import Data
from api.models.disclosure import Disclosure


class DisclosureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disclosure
        fields = ('id', 'title', 'description', 'kind', 'limit', 'user_id', 'group_id', 'data_id', 'insert_datetime')
