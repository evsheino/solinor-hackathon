# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=500)),
                ('ip_address', models.CharField(max_length=500)),
                ('location', models.CharField(max_length=100)),
                ('company_name', models.CharField(max_length=500)),
                ('webserver', models.CharField(max_length=50)),
                ('programming_language', models.CharField(max_length=50)),
                ('certificate', models.CharField(max_length=500)),
                ('certificate_authority', models.CharField(max_length=500)),
                ('html_version', models.CharField(max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
