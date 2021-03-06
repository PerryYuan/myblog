# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-05-27 05:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleModel',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=20)),
                ('desc', models.CharField(blank=True, max_length=100)),
                ('thumbnail', models.URLField(max_length=100)),
                ('content', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_time', models.DateTimeField(auto_now=True, null=True)),
                ('read_count', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.CategoryModel')),
                ('tags', models.ManyToManyField(blank=True, to='article.TagModel')),
            ],
        ),
        migrations.RemoveField(
            model_name='acticlemodel',
            name='category',
        ),
        migrations.RemoveField(
            model_name='acticlemodel',
            name='tags',
        ),
        migrations.DeleteModel(
            name='ActicleModel',
        ),
    ]
