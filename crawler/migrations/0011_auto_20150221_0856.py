# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0010_auto_20150221_0827'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteTechnology',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tech_type', models.CharField(max_length=500)),
                ('value', models.CharField(max_length=500)),
                ('site', models.ForeignKey(related_name='site_technologies', to='crawler.Site')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='sitetechnologies',
            name='site',
        ),
        migrations.DeleteModel(
            name='SiteTechnologies',
        ),
    ]
