# Generated by Django 3.2.3 on 2021-07-12 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginapp', '0013_alter_ticket_payed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='payed',
            field=models.BooleanField(default=False),
        ),
    ]
