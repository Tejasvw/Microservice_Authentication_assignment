# Generated by Django 4.2.4 on 2023-09-04 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('microservice_app', '0002_customuser_otp_customuser_otp_valid_until'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]
