from rest_framework import serializers
from core.models import Card, Game, CardSequence
from django.contrib.auth import get_user_model


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'


class CardDrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardSequence
        fields = '__all__'
