# Generated by Django 3.0.3 on 2020-02-04 16:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_cardsequence_game'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='status',
            field=models.CharField(choices=[('W', 'Won'), ('D', 'Draw'), ('NR', 'No Result')], default='NR', max_length=3),
        ),
        migrations.AlterField(
            model_name='game',
            name='won_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
