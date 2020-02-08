import random

from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response

from core.models import (Card, Game, CardSequence)
from core.models import GameStatus
from core.serializers import (CardSerializer, UserProfileSerializer,
                              GameSerializer, CardDrawSerializer)
from django.shortcuts import get_object_or_404

# create list users end point
class UserListView(generics.ListAPIView):

    # we just have to provide the queryset and the serializer.
    # ListAPIView does the rest
    queryset = get_user_model().objects.all()
    serializer_class = UserProfileSerializer


class CardListView(generics.ListAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class GameView(generics.ListCreateAPIView):

    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def post(self, request, *args, **kwargs):
        """
        To create a new Game
        """
        # get the last game if any from the games between these players
        gamex = Game.objects.filter(player1=request.data['player1'],
                                    player2=request.data['player2']).last()

        gamey = Game.objects.filter(player1=request.data['player2'],
                                    player2=request.data['player1']).last()

        if gamex:
            return Response(data=f"Game already exists between player "
                            f"{request.data['player1']} and {request.data['player2']} with id - {gamex.id}",
                            status=status.HTTP_400_BAD_REQUEST)
        if gamey:
            return Response(data=f"Game already exists between player "
                            f"{request.data['player1']} and {request.data['player2']} with id - {gamey.id}",
                            status=status.HTTP_400_BAD_REQUEST)
        data = request.data.copy()
        data['next_move_by'] = data['player1']
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GameDetailView(generics.RetrieveUpdateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def patch(self, request, *args, **kwargs):
        """this method  is for patch requests"""
        return self.partial_update(request, *args, **kwargs)


class DrawCardView(generics.ListCreateAPIView):
    queryset = CardSequence.objects.all()
    serializer_class = CardDrawSerializer

    def post(self, request, *args, **kwargs):
        game_id = request.data['game']
        user_id = request.data['user']
        game = get_object_or_404(Game, id=game_id)

        # make sure its the current players turn
        if game.next_move_by.id != user_id:
            return Response(data=f"you cannot make a move its other player's turn",
                            status=status.HTTP_400_BAD_REQUEST)

        # get already chosen cards for this game
        already_chosen = CardSequence.objects.filter(game=game_id
                                                     ).values_list('card_id', flat=True)
        # choose a card at random only from not chosen cards
        card = random.choice(Card.objects.exclude(pk__in=already_chosen))

        # copy request.data as we cannot modify it because it is immutable object
        data = request.data.copy()
        data['card'] = card.id
        # draw card and save the sequence
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # TODO: call to check does this move makes player win or not,
        #  if won update the status
        # TODO: update the next_move_by
        if game.next_move_by.id == game.player1.id:
            game.next_move_by.id = game.player2.id
        else:
            game.next_move_by.id = game.player1.id
        game.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


def get_sequence(game_id, player):
    # return the sequence in latest draw first
    seq = CardSequence.objects.filter(game=game_id, user=player
                                      ).order_by('-date_created').values_list('card__rank', flat=True)
    return seq


# def update_game(game_id, user, player_no):
#     seq = get_sequence(game_id, user)
#     game = Game.objects.get(id=game_id)
#     moves_to_win_x = 'moves_to_win_p'+str(player_no)
#     if seq[0].card.rank > seq[1].card.rank:
#         # card drawn is greater than previous
#         print(moves_to_win_x)
#         if moves_to_win_x == 'moves_to_win_p1':
#             if game.moves_to_win_p1 == 1:
#                 game.status = GameStatus.W.name
#                 game.won_by = user
#
#             game.moves_to_win_p1 -= 1
#             game.save()
#             return game
#
#         if moves_to_win_x == 'moves_to_win_p2':
#             if game.moves_to_win_p2 == 1:
#                 game.status = GameStatus.W.name
#                 game.won_by = user
#
#             game.moves_to_win_p1 -= 1
#             game.save()
#             return game


# def check_if_won(game, player):
#     seq = get_sequence(game.id, player.id)
#     for s in seq[:4]:





