from rest_framework import serializers
from api.models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'description', 'group_id.group')
