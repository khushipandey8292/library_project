# Generated by Django 5.1.6 on 2025-04-04 07:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0003_alter_borrow_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='due_date',
            field=models.DateField(default=datetime.date(2025, 4, 11)),
        ),
    ]
