# Generated by Django 4.2.1 on 2023-07-15 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthAuthorization', '0006_testimg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addnewrestaurantv2',
            name='bannar_img',
            field=models.ImageField(blank=True, default=1, upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='addnewrestaurantv2',
            name='logo',
            field=models.ImageField(blank=True, default=2, upload_to=''),
            preserve_default=False,
        ),
    ]
