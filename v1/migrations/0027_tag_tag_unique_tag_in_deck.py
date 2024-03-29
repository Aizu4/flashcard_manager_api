# Generated by Django 4.2.5 on 2024-01-09 21:20

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0026_remove_card_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
                ('deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='v1.deck')),
            ],
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(fields=('name', 'deck'), name='unique_tag_in_deck'),
        ),
    ]
