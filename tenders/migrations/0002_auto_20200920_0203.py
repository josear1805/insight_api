# Generated by Django 3.1.1 on 2020-09-20 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tender',
            name='tender_viewed',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='tender',
            name='link',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]