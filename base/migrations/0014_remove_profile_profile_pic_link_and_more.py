# Generated by Django 4.0.5 on 2022-07-01 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_alter_profile_options_profile_profile_pic_link_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='profile_pic_link',
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='profileicons/avatar.svg', upload_to=''),
        ),
    ]
