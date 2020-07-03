from django.contrib import admin

from django.contrib.admin import site

from Cursos.models import *

# Register your models here.

site.register(Question)
site.register(Lesson)
site.register(Course)
site.register(Answer)
site.register(Profile)
site.register(ProfileLesson)
