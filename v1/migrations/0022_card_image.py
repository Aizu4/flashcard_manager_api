# Generated by Django 4.2.5 on 2023-11-29 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0021_remove_card_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
