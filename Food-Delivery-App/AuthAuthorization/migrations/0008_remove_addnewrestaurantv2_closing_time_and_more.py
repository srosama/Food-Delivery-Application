# Generated by Django 4.2.1 on 2023-07-15 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AuthAuthorization', '0007_alter_addnewrestaurantv2_bannar_img_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addnewrestaurantv2',
            name='closing_time',
        ),
        migrations.RemoveField(
            model_name='addnewrestaurantv2',
            name='opening_time',
        ),
    ]
