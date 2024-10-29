# Generated by Django 5.0.1 on 2024-04-14 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_web', '0006_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='BranchPerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_name', models.CharField(max_length=32, verbose_name='分公司名称')),
                ('january_performance', models.IntegerField(verbose_name='一月份业绩')),
                ('february_performance', models.IntegerField(verbose_name='二月份业绩')),
                ('march_performance', models.IntegerField(verbose_name='三月份业绩')),
                ('april_performance', models.IntegerField(verbose_name='四月份业绩')),
                ('may_performance', models.IntegerField(verbose_name='五月份业绩')),
                ('june_performance', models.IntegerField(verbose_name='六月份业绩')),
                ('july_performance', models.IntegerField(verbose_name='七月份业绩')),
                ('august_performance', models.IntegerField(verbose_name='八月份业绩')),
                ('september_performance', models.IntegerField(verbose_name='九月份业绩')),
                ('october_performance', models.IntegerField(verbose_name='十月份业绩')),
                ('november_performance', models.IntegerField(verbose_name='十一月份业绩')),
                ('december_performance', models.IntegerField(verbose_name='十二月份业绩')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeePerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
