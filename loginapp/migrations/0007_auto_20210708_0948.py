# Generated by Django 3.2.3 on 2021-07-08 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loginapp', '0006_auto_20210708_0833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='entrace',
        ),
        migrations.AddField(
            model_name='matchentrace',
            name='match',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='loginapp.match'),
        ),
    ]
