# Generated by Django 2.0.2 on 2018-04-24 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20180424_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='circle',
            name='meta_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='circles_meta+', to='meta_info.MetaInfo', verbose_name='Circles meta data'),
        ),
    ]
