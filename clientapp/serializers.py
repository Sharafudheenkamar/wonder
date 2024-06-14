from rest_framework import serializers
from .models import Chat

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['message','from_id','to_id','created_at']
class ChatPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['message','from_id','to_id']

class ChatPostSerializerg(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['message','from_id','group_id']


