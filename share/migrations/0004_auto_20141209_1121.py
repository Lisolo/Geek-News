# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0003_keyword'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LikeCategory',
            new_name='LikeTag',
        ),
        migrations.RenameModel(
            old_name='Category',
            new_name='Tag',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='category',
            new_name='tag',
        ),
        migrations.RenameField(
            model_name='liketag',
            old_name='category',
            new_name='tag',
        ),
        migrations.RenameField(
            model_name='news',
            old_name='category',
            new_name='tag',
        ),
    ]
