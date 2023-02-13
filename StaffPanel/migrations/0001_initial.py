# Generated by Django 4.1 on 2022-09-24 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('PizzaDelivery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=7)),
                ('status', models.CharField(choices=[('not_ordered', 'not_ordered'), ('order_taken', 'order_taken'), ('order_deleted', 'order_deleted'), ('order_in_progress', 'order_in_progress'), ('order_delivery_in_progress', 'order_delivery_in_progress'), ('order_completed', 'order_completed'), ('order_cancelled', 'order_cancelled')], default='order_taken', max_length=50)),
                ('total_amount', models.CharField(default=0, max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('pizza', models.ManyToManyField(to='PizzaDelivery.pizza')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('order_id',)},
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=50)),
                ('phone', models.CharField(max_length=10)),
                ('message', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=7)),
                ('assigned_person', models.CharField(max_length=50)),
                ('is_completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratings', models.IntegerField()),
                ('feedback', models.CharField(blank=True, max_length=500)),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CancelOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('account_no', models.CharField(max_length=18)),
                ('email', models.EmailField(max_length=100)),
                ('mobile_no', models.CharField(max_length=10, null=True)),
                ('is_returned', models.BooleanField(default=False)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StaffPanel.adminorder')),
            ],
        ),
    ]
