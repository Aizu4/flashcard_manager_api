# Generated by Django 4.2.5 on 2023-11-30 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0024_alter_card_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/cards/images'),
        ),
    ]
