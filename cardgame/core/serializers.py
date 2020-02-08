from rest_framework import serializers
from core.models import (Card, Game, CardSequence,
                         GameStatus)
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
    sequence_player1 = serializers.SerializerMethodField()
    sequence_player2 = serializers.SerializerMethodField()
    card_rank = serializers.SerializerMethodField()
    card_suit = serializers.SerializerMethodField()
    game_status = serializers.SerializerMethodField()

    class Meta:
        model = CardSequence
        fields = '__all__'

    def get_sequence_player1(self, cardsequence):

        seq = CardSequence.objects.filter(
            game=cardsequence.game.id, player=cardsequence.game.player1
        ).order_by('-date_created').values_list('card__rank', 'card__suit')

        return seq

    def get_sequence_player2(self, cardsequence):

        seq = CardSequence.objects.filter(
            game=cardsequence.game.id, player=cardsequence.game.player2
        ).order_by('-date_created').values_list('card__rank', 'card__suit')

        return seq

    def get_card_rank(self, cardsequence):
        if cardsequence.card:
            card = Card.objects.get(id=cardsequence.card.id)
            return card.rank
        else:
            return None

    def get_card_suit(self, cardsequence):
        if cardsequence.card:
            card = Card.objects.get(id=cardsequence.card.id)
            return card.suit
        else:
            return None

    def get_game_status(self, cardsequence):
        if cardsequence.card:
            game = Game.objects.get(id=cardsequence.game.id)
            return game.status
        else:
            return None
