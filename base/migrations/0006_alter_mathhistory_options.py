# Generated by Django 4.0.5 on 2022-06-20 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_message_options_mathhistory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mathhistory',
            options={'ordering': ['-created']},
        ),
    ]