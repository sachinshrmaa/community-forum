# Generated by Django 3.1.7 on 2021-04-18 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210418_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_img',
            field=models.ImageField(blank=True, default='assets/default-profile-img.jpg', null=True, upload_to='profile-img/'),
        ),
    ]