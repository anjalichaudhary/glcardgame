from core.utils import create_deck
from django.core.management.base import BaseCommand
from core.models import Card


class Command(BaseCommand):
    def handle(self, *args, **options):
        card = Card.objects.all()
        if len(card) < 52:
            # TODO: Do not delete just mark as deleted and choose cards accordingly
            self.stdout.write('Deck of cards less than 52 deleting deck...')
            Card.objects.all().delete()
            self.stdout.write('Creating new deck of cards...')
            create_deck()
        else:
            return
