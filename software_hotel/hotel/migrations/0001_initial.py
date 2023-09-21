# Generated by Django 4.2.5 on 2023-09-21 19:55

import django.contrib.auth.models
import django.contrib.auth.validators
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
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('telefono', models.IntegerField()),
                ('vip', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(related_name='clientes', to='auth.group')),
                ('user_permissions', models.ManyToManyField(related_name='clientes', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('equipo_id', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Habitacion',
            fields=[
                ('habitacion_id', models.AutoField(primary_key=True, serialize=False)),
                ('disponibilidad', models.BooleanField()),
                ('numero_habitacion', models.IntegerField()),
                ('metros_cuadrados', models.IntegerField()),
                ('precio', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('hotel_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('direccion', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Metodo_pago',
            fields=[
                ('pago_id', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('servicio_id', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_habitacion',
            fields=[
                ('tipo_habitacion_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('equipos', models.ManyToManyField(to='hotel.equipo')),
                ('servicios', models.ManyToManyField(to='hotel.servicio')),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('reserva_id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_entrada', models.DateField()),
                ('fecha_salida', models.DateField()),
                ('cantidad_personas', models.IntegerField()),
                ('precio_final', models.IntegerField()),
                ('fecha_hora_pago', models.DateTimeField(default=django.utils.timezone.now)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.cliente')),
                ('habitacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.habitacion')),
                ('pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.metodo_pago')),
            ],
        ),
        migrations.AddField(
            model_name='habitacion',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel'),
        ),
        migrations.AddField(
            model_name='habitacion',
            name='tipo_habitacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.tipo_habitacion'),
        ),
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('telefono', models.IntegerField()),
                ('role', models.CharField(choices=[('TI', 'TI'), ('Administrador de hotel', 'Administrador de hotel'), ('Administrador de reserva', 'Administrador de reserva'), ('Empleado', 'Empleado')], default='Administrador de hotel', max_length=24)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(related_name='administradores', to='auth.group')),
                ('user_permissions', models.ManyToManyField(related_name='administradores', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]