# Generated by Django 5.0.6 on 2024-07-05 15:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_rename_title_category_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='servings_time',
            new_name='servings',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='category',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='recipes.category'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cover',
            field=models.ImageField(blank=True, default='', upload_to='recipes/covers/%Y/%m/%d'),
        ),
    ]
