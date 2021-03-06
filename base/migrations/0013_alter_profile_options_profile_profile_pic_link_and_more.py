# Generated by Django 4.0.5 on 2022-07-01 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_rename_score_profile_points_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['-points']},
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_pic_link',
            field=models.CharField(default='profileicons/avatar.svg', max_length=50),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(default='Hello World!', max_length=120),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default=models.CharField(default='profileicons/avatar.svg', max_length=50), upload_to=''),
        ),
    ]
