# Generated by Django 2.0 on 2018-09-20 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DNSmisconfiguration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressIPv4',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(protocol='IPv4')),
            ],
        ),
        migrations.CreateModel(
            name='AddressIPv6',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(protocol='IPv6')),
            ],
        ),
        migrations.CreateModel(
            name='KnownNameServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(default='', max_length=512)),
                ('known_server', models.CharField(default='', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('host_name', models.CharField(default='', max_length=256, primary_key=True, serialize=False)),
                ('description', models.CharField(default='', max_length=512)),
                ('original_domain', models.CharField(default='', max_length=256)),
            ],
        ),
        migrations.RemoveField(
            model_name='addressip',
            name='url',
        ),
        migrations.DeleteModel(
            name='AddressIP',
        ),
        migrations.DeleteModel(
            name='AddressURL',
        ),
        migrations.AddField(
            model_name='knownnameserver',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DNSmisconfiguration.Server'),
        ),
        migrations.AddField(
            model_name='addressipv6',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DNSmisconfiguration.Server'),
        ),
        migrations.AddField(
            model_name='addressipv4',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DNSmisconfiguration.Server'),
        ),
        migrations.AlterUniqueTogether(
            name='knownnameserver',
            unique_together={('server', 'domain')},
        ),
    ]