# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0008_auto_20150221_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='location',
            field=models.ForeignKey(related_name='sites', to='crawler.Location', null=True),
            preserve_default=True,
        ),
    ]
