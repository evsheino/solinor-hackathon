# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteTechnologies',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('webserver', models.CharField(max_length=50, blank=True)),
                ('programming_language', models.CharField(max_length=50, blank=True)),
                ('certificate', models.CharField(max_length=500, blank=True)),
                ('certificate_authority', models.CharField(max_length=500, blank=True)),
                ('html_version', models.CharField(max_length=500, blank=True)),
                ('site', models.ForeignKey(to='crawler.Site')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='site',
            name='certificate',
        ),
        migrations.RemoveField(
            model_name='site',
            name='certificate_authority',
        ),
        migrations.RemoveField(
            model_name='site',
            name='html_version',
        ),
        migrations.RemoveField(
            model_name='site',
            name='programming_language',
        ),
        migrations.RemoveField(
            model_name='site',
            name='webserver',
        ),
        migrations.AlterField(
            model_name='site',
            name='company_name',
            field=models.CharField(max_length=500, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='location',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
    ]
