# Generated by Django 2.2.16 on 2022-07-21 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GenreTitle',
            new_name='GenreToTitle',
        ),
        migrations.AlterModelOptions(
            name='genretotitle',
            options={'verbose_name': 'Жанр Произведения', 'verbose_name_plural': 'Жанры Произведений'},
        ),
        migrations.RemoveConstraint(
            model_name='title',
            name='unique_title',
        ),
    ]
