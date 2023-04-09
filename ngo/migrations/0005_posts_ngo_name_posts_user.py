# Generated by Django 4.1.3 on 2023-04-07 13:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ngo', '0004_remove_posts_ngo_name_remove_posts_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='ngo_name',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='ngo.profile'),
        ),
        migrations.AddField(
            model_name='posts',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]