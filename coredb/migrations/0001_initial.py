# Generated by Django 3.0.2 on 2020-01-24 20:05

import coredb.models
from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('gender', models.CharField(choices=[('U', 'Not recorded'), ('M', 'Man'), ('F', 'Woman'), ('O', 'Something else')], default='U', max_length=1)),
                ('pronouns', models.CharField(blank=True, max_length=64)),
                ('phone', models.CharField(blank=True, max_length=16)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', coredb.models.PersonManager()),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address1', models.CharField(blank=True, max_length=128)),
                ('address2', models.CharField(blank=True, max_length=128)),
                ('city', models.CharField(blank=True, max_length=128)),
                ('state', models.CharField(blank=True, max_length=2)),
                ('zipcode', models.CharField(blank=True, max_length=16)),
                ('country', models.CharField(blank=True, max_length=128)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('code', models.CharField(max_length=32, unique=True)),
                ('type', models.CharField(choices=[('space', 'Coworking Space'), ('vendor', 'Product Vendor'), ('consultant', 'Consultantancy'), ('nonprofit', 'Non-Profit'), ('coop', 'Co-Operative'), ('collective', 'Collective'), ('other', 'Other')], default='other', max_length=16)),
                ('description', models.TextField(blank=True)),
                ('phone', models.CharField(blank=True, max_length=16)),
                ('email', models.EmailField(blank=True, max_length=100, unique=True)),
                ('created_ts', models.DateTimeField(auto_now_add=True)),
                ('updated_ts', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='coredb.Location')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('github', 'github'), ('linkedin', 'linkedin'), ('personal', 'personal'), ('facebook', 'facebook'), ('instagram', 'instagram'), ('blog', 'blog'), ('other', 'other')], default='other', max_length=16)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('founder', 'Founder'), ('owner', 'Owner'), ('employee', 'Employee'), ('volunteer', 'Volunteer'), ('vendor', 'Product Vendor'), ('consultant', 'Consultant'), ('other', 'Other')], default='other', max_length=16)),
                ('start_day', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('start_month', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('start_year', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('end_day', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('end_month', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('end_year', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coredb.Project')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='websites',
            field=models.ManyToManyField(blank=True, to='coredb.Website'),
        ),
        migrations.CreateModel(
            name='EmailAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('created_ts', models.DateTimeField(auto_now_add=True)),
                ('verif_key', models.CharField(max_length=40)),
                ('verified_ts', models.DateTimeField(blank=True, default=None, null=True)),
                ('remote_addr', models.GenericIPAddressField(blank=True, null=True)),
                ('remote_host', models.CharField(blank=True, max_length=255)),
                ('is_primary', models.BooleanField(default=False)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emails', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='coredb.Location'),
        ),
        migrations.AddField(
            model_name='person',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='person',
            name='websites',
            field=models.ManyToManyField(blank=True, to='coredb.Website'),
        ),
    ]
