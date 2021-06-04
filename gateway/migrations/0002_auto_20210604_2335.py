# Generated by Django 3.1.7 on 2021-06-04 23:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gateway', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='router',
            name='step',
        ),
        migrations.AddField(
            model_name='router',
            name='arrangement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='router_arrangement', to='gateway.arrangement', verbose_name='编排'),
        ),
    ]
