# Generated by Django 2.1.5 on 2019-03-30 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_task_taskdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.SmallIntegerField(choices=[(0, 'cmd'), (1, 'file_transfer')]),
        ),
    ]
