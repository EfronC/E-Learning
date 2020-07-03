# Generated by Django 3.0.8 on 2020-07-02 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cursos', '0003_auto_20200702_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='prev_course',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lesson',
            name='prev_lesson',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='completed_courses',
            field=models.ManyToManyField(blank=True, related_name='answers', to='Cursos.Course'),
        ),
    ]
