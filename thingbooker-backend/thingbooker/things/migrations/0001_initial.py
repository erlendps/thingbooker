# Generated by Django 4.2.8 on 2024-01-14 16:28

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import thingbooker.things.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Thing',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField(max_length=1000)),
                ('picture', models.ImageField(blank=True, null=True, upload_to=thingbooker.things.models.thing_picture_upload_path, validators=[django.core.validators.validate_image_file_extension])),
                ('members', models.ManyToManyField(related_name='things', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_things', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('can_manage_booking', 'User can manage (accept/decline) booking')],
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('num_people', models.PositiveIntegerField(default=1, verbose_name='Number of guests using the thing')),
                ('status', models.TextField(choices=[('declined', 'Booking is declined'), ('accepted', 'Booking is accepted'), ('waiting', 'Booking is waiting for approval')], default='waiting', max_length=10)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('booker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL)),
                ('thing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='things.thing')),
            ],
            options={
                'ordering': ['thing', 'start_date'],
            },
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('short', models.CharField(max_length=150)),
                ('description', models.TextField(max_length=1000)),
                ('thing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rules', to='things.thing')),
            ],
            options={
                'order_with_respect_to': 'thing',
            },
        ),
        migrations.AddConstraint(
            model_name='booking',
            constraint=models.CheckConstraint(check=models.Q(('end_date__gt', models.F('start_date'))), name='end_date__gt__start_date'),
        ),
    ]
