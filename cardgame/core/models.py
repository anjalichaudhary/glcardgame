from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from core.managers import UserManager
from enum import Enum


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom player model that supports using email instead of username """

    username = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        ordering = ('id', )

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.username


class Suit(Enum):
    SPADE = "Spades"
    CLUB = "Clubs"
    DIAMOND = "Diamond"
    HEART = "Heart"
    EXTRA = "Extra"


class Card(models.Model):
    suit = models.CharField(
        max_length=10,
        choices=[(tag.name, tag.value) for tag in Suit],
        default=Suit.EXTRA.name
    )
    rank = models.CharField(max_length=5)

    def __str__(self):
        return f'{self.suit} - {self.rank}'


class GameStatus(Enum):
    """Enum for different types of topic"""

    NR = "No Result"
    W = "Won"
    D = "Draw"


class Game(models.Model):
    player1 = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                related_name="player1")
    player2 = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                related_name="player2")
    next_move_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                     related_name='move_by', blank=True,
                                     null=True)
    status = models.CharField(
        max_length=3,
        choices=[(tag.name, tag.value) for tag in GameStatus],
        default=GameStatus.NR.name
    )
    won_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None,
                               null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'game b/w {self.player1} & {self.player2}'


class CardSequence(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Card - {self.card} drawn by {self.player}'
