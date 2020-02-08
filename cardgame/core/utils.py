from core.models import Card


def create_deck():
    """
    Create a list of playing cards in our database
    :return:
    """
    suits = ["SPADE", "CLUB", "DIAMOND", "HEART"]
    ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    cards = [Card(suit=suit, rank=rank) for rank in ranks for suit in suits]
    Card.objects.bulk_create(cards)
