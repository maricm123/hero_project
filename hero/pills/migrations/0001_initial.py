# Generated by Django 4.2.11 on 2024-03-25 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot', models.CharField(max_length=512)),
                ('name', models.CharField(max_length=512)),
                ('dosage', models.CharField(max_length=512)),
                ('expires', models.DateField()),
                ('passcode_required', models.BooleanField(default=True)),
                ('form', models.CharField(max_length=512)),
                ('exact_pill_count', models.IntegerField(null=True)),
                ('max_manual_doses', models.IntegerField(null=True)),
                ('device_config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pills', to='config.config')),
            ],
        ),
    ]
