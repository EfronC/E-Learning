from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
	name = models.CharField(max_length=100)
	question_text = models.TextField(default=False, blank=False, null=False)
	multiple = models.BooleanField(default=False, blank=False, null=False)
	allselected = models.BooleanField(default=True, blank=False, null=False)
	options = models.TextField(blank=False, null=True)
	score = models.IntegerField(blank=False, null=True)
	active = models.BooleanField(default=True, blank=False, null=False)
	creation_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

class Lesson(models.Model):
	name = models.CharField(max_length=100)
	questions = models.ManyToManyField(Question, related_name='questions')
	approval_score = models.IntegerField(blank=False, null=True)
	next_lesson = models.IntegerField(blank=True, null=True)
	prev_lesson = models.IntegerField(blank=True, null=True)
	first = models.BooleanField(default=False, blank=False, null=False)
	active = models.BooleanField(default=True, blank=False, null=False)
	creation_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

class Course(models.Model):
	name = models.CharField(max_length=100)
	lessons = models.ManyToManyField(Lesson, related_name='lesson')
	next_course = models.IntegerField(blank=True, null=True)
	prev_course = models.IntegerField(blank=True, null=True)
	first = models.BooleanField(default=False, blank=False, null=False)
	active = models.BooleanField(default=True, blank=False, null=False)
	creation_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '%s - %s' % (self.name, self.id)

class Answer(models.Model):
	question = models.ForeignKey(Question, null=True, blank=False, on_delete=models.PROTECT)
	answer = models.TextField(blank=False, null=True)
	correct = models.BooleanField(default=False, blank=False, null=False)
	active = models.BooleanField(default=True, blank=False, null=False)
	creation_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.question.name

class Profile(models.Model):
	user = models.ForeignKey(User, related_name='perfil_usr', on_delete=models.PROTECT)
	completed_courses = models.ManyToManyField(Course, related_name='answers', blank=True)
	active = models.BooleanField(default=True, blank=False, null=False)
	creation_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '%s' % self.user.username

	class Meta:
		permissions = (
			('maestro', 'Permiso para crear y administrar cursos, lecciones, y preguntas'),
		)

class ProfileLesson(models.Model):
	profile = models.ForeignKey(Profile, related_name='perfilu', on_delete=models.PROTECT)
	lesson = models.ForeignKey(Lesson, related_name='lessonu', on_delete=models.PROTECT)
	answers = models.ManyToManyField(Answer, related_name='answers')
	completed = models.BooleanField(default=False, blank=False, null=False)
	active = models.BooleanField(default=True, blank=False, null=False)
	creation_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '%s - %s' % (self.lesson.name, self.profile.user.username)
