# Generated by Django 5.1.1 on 2024-09-26 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0003_car_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='category',
            field=models.CharField(choices=[('SUV', 'Внедорожник'), ('SEDAN', 'Седан'), ('COUPE', 'Купе'), ('HATCHBACK', 'Хэтчбек')], default='SEDAN', max_length=100),
        ),
    ]
