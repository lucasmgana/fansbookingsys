# Generated by Django 3.2.3 on 2021-07-07 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loginapp', '0004_remove_matchentrace_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchentrace',
            name='match',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='loginapp.match'),
        ),
    ]
