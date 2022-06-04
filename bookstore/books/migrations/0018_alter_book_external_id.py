# Generated by Django 4.0.5 on 2022-06-04 09:25

from django.db import migrations
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0017_remove_book_external_id1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='external_id',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22),
        ),
    ]