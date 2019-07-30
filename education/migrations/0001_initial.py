# Generated by Django 2.1.3 on 2019-07-28 14:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lecture_order', models.CharField(blank=True, max_length=120, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('creationDate', models.DateTimeField(auto_now_add=True)),
                ('education_year', models.CharField(blank=True, max_length=120, null=True)),
                ('education_season', models.CharField(blank=True, max_length=120, null=True)),
                ('is_exist', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Sınıf Adı')),
                ('education_year', models.CharField(choices=[('2018-2019', '2018-2019'), ('2019-2020', '2019-2020')], default='2018-2019', max_length=128, verbose_name='Eğitim Yılı')),
                ('creationDate', models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')),
                ('modificationDate', models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu', models.TextField(blank=True, max_length=18500, null=True, verbose_name='Yemek Menüsü')),
                ('food_date', models.DateField(verbose_name='Yemek Tarihi')),
                ('creation_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=1280, null=True)),
                ('creationDate', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, null=True)),
                ('url', models.CharField(blank=True, max_length=120, null=True)),
                ('is_parent', models.BooleanField(default=True)),
                ('is_show', models.BooleanField(default=True)),
                ('fa_icon', models.CharField(blank=True, max_length=120, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='education.Menu')),
                ('permission', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Permission')),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profileImage', models.ImageField(blank=True, null=True, upload_to='profile/', verbose_name='Profil Resmi')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Adres')),
                ('mobilePhone', models.CharField(max_length=120, verbose_name='Telefon Numarası')),
                ('gender', models.CharField(choices=[('Erkek', 'Erkek'), ('Kadın', 'Kadın')], default='Erkek', max_length=128, verbose_name='Cinsiyeti')),
                ('tc', models.CharField(blank=True, max_length=128, null=True, verbose_name='T.C. Kimlik Numarası')),
                ('birthDate', models.DateField(null=True, verbose_name='Doğum Tarihi')),
                ('creationDate', models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')),
                ('modificationDate', models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True, verbose_name='Ayar Adı')),
                ('value', models.CharField(blank=True, max_length=120, null=True, verbose_name='Ayar Değeri')),
                ('title', models.CharField(blank=True, max_length=120, null=True, verbose_name='Ayar Başlığı')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profileImage', models.ImageField(blank=True, null=True, upload_to='profile/', verbose_name='Profil Resmi')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Adres')),
                ('mobilePhone', models.CharField(max_length=120, verbose_name='Telefon Numarası')),
                ('studentNumber', models.CharField(max_length=128, verbose_name='Öğrenci Numarası')),
                ('gender', models.CharField(choices=[('Erkek', 'Erkek'), ('Kadın', 'Kadın')], default='Erkek', max_length=128, verbose_name='Cinsiyeti')),
                ('tc', models.CharField(blank=True, max_length=128, null=True, verbose_name='T.C. Kimlik Numarası')),
                ('birthDate', models.DateField(null=True, verbose_name='Doğum Tarihi')),
                ('creationDate', models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')),
                ('modificationDate', models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')),
                ('isAddedToClass', models.BooleanField(default=False)),
                ('parents', models.ManyToManyField(to='education.Parent')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('student_add', 'Öğrenci Ekle'), ('student_list', 'Öğrenci Liste'), ('update_student', 'Öğrenci Güncelle')),
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profileImage', models.ImageField(blank=True, null=True, upload_to='profile/', verbose_name='Profil Resmi')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Adres')),
                ('mobilePhone', models.CharField(max_length=120, verbose_name='Telefon Numarası')),
                ('gender', models.CharField(choices=[('Erkek', 'Erkek'), ('Kadın', 'Kadın')], default='Erkek', max_length=128, verbose_name='Cinsiyeti')),
                ('tc', models.CharField(blank=True, max_length=128, null=True, verbose_name='T.C. Kimlik Numarası')),
                ('birthDate', models.DateField(null=True, verbose_name='Doğum Tarihi')),
                ('creationDate', models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')),
                ('modificationDate', models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('teacher_add', 'Öğretmen Ekle'), ('teacher_list', 'Öğretmen Liste'), ('update_teacher', 'Öğretmen Güncelle')),
            },
        ),
        migrations.AddField(
            model_name='class',
            name='students',
            field=models.ManyToManyField(to='education.Student', verbose_name='Öğrenci'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='class_object',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='education.Class'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.Student'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='taken_by_who',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
