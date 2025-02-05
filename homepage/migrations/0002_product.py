# Generated by Django 4.2.5 on 2023-09-19 17:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(max_length=100)),
                ('pcategory', models.CharField(choices=[('V', 'Vegetables'), ('F', 'Fruits'), ('S', 'Sweets'), ('BI', 'Bake Items'), ('SD', 'Soft Drinks'), ('MI', 'Milk Items')], max_length=2)),
                ('pdescription', models.TextField()),
                ('selling_price', models.FloatField()),
                ('discount_price', models.FloatField()),
                ('discount_percent', models.IntegerField()),
                ('image1', models.ImageField(upload_to='productimg')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='productimg')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='productimg')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
