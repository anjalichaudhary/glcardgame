# Generated by Django 3.0.3 on 2020-02-04 21:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_game_next_move_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='next_move_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='move_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
