# Generated by Django 5.1.6 on 2025-03-19 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0004_remove_booktable_available_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='issue_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
