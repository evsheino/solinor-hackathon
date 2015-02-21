# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0007_location_population'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='population',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
