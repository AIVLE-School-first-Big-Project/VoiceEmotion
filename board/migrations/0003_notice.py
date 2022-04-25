# Generated by Django 4.0.4 on 2022-04-21 01:06

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_rename_user_id_board_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=45)),
                ('content', models.CharField(max_length=400)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('username', models.CharField(default='관리자', max_length=45)),
            ],
            options={
                'db_table': 'notice',
            },
        ),
    ]
