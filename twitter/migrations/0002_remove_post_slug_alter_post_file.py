# Generated by Django 4.1 on 2022-08-27 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='slug',
        ),
        migrations.AlterField(
            model_name='post',
            name='file',
            field=models.FileField(blank=True, upload_to='files_posts/%Y/%m/%d', verbose_name='Файлы'),
        ),
    ]