# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0002_auto_20150220_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitetechnologies',
            name='site',
            field=models.OneToOneField(to='crawler.Site'),
            preserve_default=True,
        ),
    ]
