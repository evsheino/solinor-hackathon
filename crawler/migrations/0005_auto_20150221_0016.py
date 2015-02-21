# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0004_auto_20150221_0011'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country', models.CharField(max_length=2)),
                ('city', models.CharField(max_length=100, db_index=True)),
                ('city_accent', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=10, null=True)),
                ('population', models.CharField(max_length=20, null=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='site',
            name='location',
            field=models.ForeignKey(to='crawler.Location', null=True),
            preserve_default=True,
        ),
    ]
