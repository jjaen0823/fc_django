# Generated by Django 3.1.5 on 2021-01-27 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fcuser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('password', models.CharField(max_length=64, verbose_name='Password')),
                ('register_date', models.DateTimeField(auto_now_add=True, verbose_name='Register Date')),
            ],
            options={
                'verbose_name': 'fcuser',
                'verbose_name_plural': 'fcuser',
                'db_table': 'fc_fcuser',
            },
        ),
    ]
