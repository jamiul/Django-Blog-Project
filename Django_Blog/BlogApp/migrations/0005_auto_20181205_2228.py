# Generated by Django 2.1.4 on 2018-12-05 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0004_author_profile_pic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='profile_pic',
            new_name='profile_picture',
        ),
    ]