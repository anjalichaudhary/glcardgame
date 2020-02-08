# Generated by Django 3.0.3 on 2020-02-04 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200204_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='suit',
            field=models.CharField(choices=[('SPADE', 'Spades'), ('CLUB', 'Clubs'), ('DIAMOND', 'Diamond'), ('HEART', 'Heart'), ('EXTRA', 'Extra')], default='EXTRA', max_length=10),
        ),
    ]