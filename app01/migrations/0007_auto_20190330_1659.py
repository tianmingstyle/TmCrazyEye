# Generated by Django 2.1.5 on 2019-03-30 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_auto_20190330_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskdetail',
            name='result',
            field=models.TextField(blank=True, max_length=256, null=True),
        ),
    ]
