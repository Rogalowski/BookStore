# Generated by Django 4.0.5 on 2022-06-04 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_alter_book_external_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='external_id',
            field=models.UUIDField(default='591ef', editable=False),
        ),
    ]
