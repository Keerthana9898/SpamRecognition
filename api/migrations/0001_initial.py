# Generated by Django 4.2.4 on 2024-06-15 13:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('phone_number', models.CharField(max_length=10, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='customuser_set', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='customuser_set', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Spam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=10, unique=True)),
                ('reason', models.TextField()),
                ('reported_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_spams', to='api.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='Global',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=10)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('spam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.spam')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='api.customuser')),
            ],
        ),
        migrations.AddIndex(
            model_name='spam',
            index=models.Index(fields=['phone_number'], name='api_spam_phone_n_200505_idx'),
        ),
        migrations.AddIndex(
            model_name='global',
            index=models.Index(fields=['name'], name='api_global_name_48ed83_idx'),
        ),
        migrations.AddIndex(
            model_name='global',
            index=models.Index(fields=['phone_number'], name='api_global_phone_n_c1a7c2_idx'),
        ),
        migrations.AddIndex(
            model_name='contact',
            index=models.Index(fields=['name'], name='api_contact_name_397b16_idx'),
        ),
        migrations.AddIndex(
            model_name='contact',
            index=models.Index(fields=['phone_number'], name='api_contact_phone_n_20dc54_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='contact',
            unique_together={('user', 'phone_number')},
        ),
    ]