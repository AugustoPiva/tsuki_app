# Generated by Django 2.1.7 on 2019-05-13 23:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tsuki_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listaprecios',
            name='id',
            field=models.SlugField(max_length=256, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='productosordenados',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tsuki_app.Listaprecios'),
        ),
    ]
