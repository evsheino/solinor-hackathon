# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0012_auto_20150221_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='country_full',
            field=models.CharField(default=b'', max_length=50),
            preserve_default=True,
        ),
    ]
