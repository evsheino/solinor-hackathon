# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0003_auto_20150220_2006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='site',
            name='location',
        ),
        migrations.AlterField(
            model_name='sitetechnologies',
            name='site',
            field=models.OneToOneField(related_name='site_technologies', to='crawler.Site'),
            preserve_default=True,
        ),
    ]
