# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0009_auto_20150221_0305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitetechnologies',
            name='certificate',
        ),
        migrations.RemoveField(
            model_name='sitetechnologies',
            name='certificate_authority',
        ),
        migrations.RemoveField(
            model_name='sitetechnologies',
            name='html_version',
        ),
        migrations.RemoveField(
            model_name='sitetechnologies',
            name='programming_language',
        ),
        migrations.RemoveField(
            model_name='sitetechnologies',
            name='webserver',
        ),
        migrations.AddField(
            model_name='site',
            name='backend_framework',
            field=models.CharField(max_length=500, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='site',
            name='certificate',
            field=models.CharField(max_length=500, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='site',
            name='certificate_authority',
            field=models.CharField(max_length=500, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='site',
            name='frontend_framework',
            field=models.CharField(max_length=500, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='site',
            name='frontend_language',
            field=models.CharField(max_length=500, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='site',
            name='html_version',
            field=models.CharField(max_length=500, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='site',
            name='logo_url',
            field=models.CharField(max_length=500, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='site',
            name='programming_language',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='site',
            name='webserver',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
    ]
