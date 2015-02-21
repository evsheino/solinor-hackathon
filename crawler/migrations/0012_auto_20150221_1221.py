# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0011_auto_20150221_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitetechnology',
            name='value',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
