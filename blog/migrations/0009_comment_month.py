# Generated by Django 3.2 on 2022-06-24 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='month',
            field=models.CharField(choices=[('JAN', 'January'), ('FEB', 'February'), ('MAR', 'March'), ('APR', 'April'), ('MAY', 'May')], default='APR', max_length=3),
        ),
    ]
