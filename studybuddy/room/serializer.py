from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Room, Topic, Message



class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
        ]  


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name']


class RoomSerializer(serializers.ModelSerializer):
    host = UserSummarySerializer(read_only=True)

    class Meta:
        model = Room
        fields = [
        'id',
        'name',
        'slug',
        'description',
        'created',
        'updated',
        'host',
        'topic',
    ]

    read_only_fields = [
        'id',
        'created',
        'updated',
        'host',
    ]




class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = [
            "id",
            "body",
            "created",
            "updated",
            "user",
            "room",
        ]

        read_only_fields = [
            "id",
            "created",
            "updated",
            "user",
        ]



class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = [
            "id",
            "username",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
