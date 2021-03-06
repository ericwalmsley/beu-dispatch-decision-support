# Generated by Django 4.0.2 on 2022-02-22 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dds', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dispatchlevel',
            old_name='dl_userSet',
            new_name='Dispatch_Level_Captain_Override',
        ),
        migrations.RenameField(
            model_name='dispatchlevel',
            old_name='fdra',
            new_name='Fire_Danger_Rating_Area',
        ),
        migrations.RenameField(
            model_name='dispatchlevel',
            old_name='obs_time',
            new_name='observation_time',
        ),
        migrations.AddField(
            model_name='dispatchlevel',
            name='Reason_for_changing_dispatch_level',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
