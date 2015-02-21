# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0005_auto_20150221_0016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='population',
        ),
    ]
