# Generated by Django 4.2.1 on 2023-07-14 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthAuthorization', '0003_addnewrestaurantv2_delete_addnewrestaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addnewrestaurantv2',
            name='bannar_img',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='addnewrestaurantv2',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
