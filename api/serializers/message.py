from rest_framework import serializers
from api.models.data import Data
from api.models.message import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'title', 'description', 'disclosure_id', 'user1_id', 'user2_id',
                  'data_id', 'is_read', 'insert_datetime')
