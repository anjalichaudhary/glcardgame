import random

from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response

from core.models import (Card, Game, CardSequence)
from core.models import GameStatus
from core.serializers import (CardSerializer, UserProfileSerializer,
                              GameSerializer, CardDrawSerializer)
from django.shortcuts import get_object_or_404
from django.db.models import Q


class UserListView(generics.ListAPIView):
    # we just have to provide the queryset and the serializer.
    # ListAPIView does the rest
    queryset = get_user_model().objects.all()
    serializer_class = UserProfileSerializer


class CardListView(generics.ListAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class GameDetailView(generics.RetrieveUpdateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def patch(self, request, *args, **kwargs):
        """this method  is for patch requests"""
        return self.partial_update(request, *args, **kwargs)


def get_user(username):
    """
    Return a player if username exists else
    create the player with username and return
    :param username:
    :return: player.id
    """
    user = get_user_model().objects.filter(username=username).first()
    if user:
        return user
    # create the player
    else:
        user = get_user_model().objects.create(username=username)
        if user:
            return user
        else:
            return None


class GameView(generics.ListCreateAPIView):

    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def post(self, request, *args, **kwargs):
        """
        To create a new Game
        """
        player1 = get_user(username=request.data['username1'])
        player2 = get_user(username=request.data['username2'])

        if player1 is None or player2 is None:
            return Response(data=f"An error occurred while creating players",
                            status=status.HTTP_400_BAD_REQUEST)

        # get the last game if any from the games between these players
        game = Game.objects.filter(Q(player1=player1.id,
                                   player2=player2.id) |
                                   Q(player1=player2.id,
                                   player2=player1.id)).last()

        if game:
            return Response(data=f"Game already exists between player "
                            f"{request.data['player1']} and {request.data['player2']} with id - {game.id}",
                            status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['next_move_by'] = player1.id
        data['player1'] = player1.id
        data['player2'] = player2.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DrawCardView(generics.ListCreateAPIView):
    queryset = CardSequence.objects.all()
    serializer_class = CardDrawSerializer

    def post(self, request, *args, **kwargs):
        game_id = request.data['game']
        player_id = request.data['player']

        # check player belongs to the game
        game = Game.objects.filter(Q(id=game_id, player1=player_id) |
                                   Q(id=game_id, player2=player_id)).first()

        if not game:
            return Response(data=f"Player {player_id} does not belong to game {game_id}",
                            status=status.HTTP_400_BAD_REQUEST)

        player = get_object_or_404(get_user_model(), id=player_id)
        # make sure its the current players turn
        if game.next_move_by.id != player_id:
            return Response(data=f"you cannot make a move its other player's turn",
                            status=status.HTTP_400_BAD_REQUEST)

        # get already chosen cards for this game
        already_chosen = CardSequence.objects.filter(game=game_id
                                                     ).values_list('card_id', flat=True)

        if len(already_chosen) == 52:
            """All cards are exhausted Game is draw"""
            game.status = GameStatus.D.name
            game.save()
            return Response(data=f'Match is Draw',
                            status=status.HTTP_200_OK)

        # choose a card at random only from not chosen cards
        card = random.choice(Card.objects.exclude(pk__in=already_chosen))

        # copy request.data as we cannot modify it because it is immutable object
        data = request.data.copy()
        data['card'] = card.id
        # draw card and save the sequence
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # call to check does this move makes player win or not,
        #  if won update the status else update the next_move_by
        has_won_game = has_won(game=game, player=player)

        if has_won_game:
            game.status = GameStatus.W.name
            game.won_by = player
            game.save()
            return Response(data={"data": serializer.data,
                                  "message": f"Game won by {player.username}"},
                            status=status.status.HTTP_200_OK)
        else:
            game.next_move_by = get_next_player(game)
            game.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


def get_next_player(game):
    if game.next_move_by.id == game.player1.id:
        return game.player2
    else:
        return game.player1


def get_sequence(game_id, player):
    """
    get the sequence of card drawn in the decending order of their date_created
    i.e latest card value first
    :param game_id:
    :param player:
    :return: seq of ranks i.e card value
    """
    # return the sequence in latest draw first
    seq = CardSequence.objects.filter(
        game=game_id, player=player).order_by('-date_created')\
        .values_list('card__rank', flat=True)
    return seq


def has_won(game, player):
    """
    lets say last 4 moves are 13 9 3 3
                13 - is the value of last(latest) move,
                9 value before it and so on.
    so the last 4 values sequence (13, 9, 3, 3) should be in decreasing order

    :param game: game object for which the game is being played for
    :param player: the player who is playing this move
    :return: check and return if the player has won or not -> Boolean value
    """
    seq = get_sequence(game.id, player.id)

    # if less than 4 sequences
    if len(seq) < 4:
        return False
    latest_four = seq[:4]
    is_decreasing = all(int(latest_four[i]) >= int(latest_four[i+1])
                        for i in range(len(latest_four)-1)
                        )
    if is_decreasing:
        return True
    else:
        return False





