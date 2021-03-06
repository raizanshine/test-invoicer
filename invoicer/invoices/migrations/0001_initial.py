# Generated by Django 3.1.5 on 2021-02-01 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, help_text='Сумма к оплате', max_digits=18, verbose_name='Сумма')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('currency', models.CharField(choices=[('EUR', 'Евро'), ('USD', 'Доллары'), ('RUB', 'Рубли')], default=None, max_length=9, verbose_name='Валюта')),
                ('payment_type', models.CharField(default=None, max_length=128, verbose_name='Платежная система')),
            ],
        ),
    ]
