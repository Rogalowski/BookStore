# Generated by Django 4.0.5 on 2022-06-04 08:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_alter_book_external_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='external_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]