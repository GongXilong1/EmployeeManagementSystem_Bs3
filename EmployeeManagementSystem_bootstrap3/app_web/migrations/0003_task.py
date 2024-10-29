# Generated by Django 5.0.1 on 2024-04-02 06:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_web', '0002_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_level', models.SmallIntegerField(choices=[(1, '紧急'), (2, '重要'), (3, '临时')], default=1, verbose_name='级别')),
                ('task_title', models.CharField(max_length=64, verbose_name='任务标题')),
                ('task_detail', models.TextField(verbose_name='任务详情')),
                ('task_responsible_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_web.admin', verbose_name='负责人')),
            ],
        ),
    ]
