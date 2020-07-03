from __future__ import unicode_literals

import datetime
import json

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from Cursos.models import *

def build_dict(seq, key):
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))

def createQuestion(data):
	multiple = data.get("multiple", 0)
	question_text = data["question_text"]
	score = data["score"]
	alls = data.get("alls", 0)
	options = data["options"]
	if question_text and score:
		if int(multiple) == 1:
			multiple = True
			if int(alls) == 1:
				alls = True
			else:
				alls = False
		else:
			multiple=False
			alls=False
		"""
		try:
			optionscheck = json.loads(options)
		except Exception as e:
			return (False, 0)
		"""

		q = Question.objects.create(
			question_text = question_text,
			multiple = multiple,
			allselected = alls,
			options = json.dumps(options),
			score = int(score),
		)
		q.name = "Q"+str(q.id)
		q.save()

		return (True, q)
	return (False, 0)

def createLesson(data):
	name = data["name"]
	approval_score = data["approval_score"]
	prev_lesson = data.get("prev_lesson", None)
	if name and approval_score:
		l = Lesson.objects.create(
			name = name,
			approval_score= approval_score,
			)
		if prev_lesson:
			pl = Lesson.objects.get(id=prev_lesson)
			l.next_lesson = pl.next_lesson
			l.prev_lesson = pl.id
			pl.next_lesson = l.id
			pl.save()

		for i in data["questions"]:
			r = createQuestion(i)
			if r[0]:
				l.questions.add(r[1])
		l.save()
		return (True, l)
	return (False, 0)

def checkCourse(lesson, profile):
	course = Course.objects.filter(lessons__in=[lesson]).first()

	pls = ProfileLesson.objects.filter(profile=profile, lesson__in=course.lessons.all())
	comp = True

	for i in pls:
		if not i.completed:
			comp = False

	if comp and len(pls) == len(course.lessons.all()):
		profile.completed_courses.add(course)
		profile.save()
		return True
	else:
		return False

def checkLessonAvailability(lesson, profile):
	course = Course.objects.filter(lessons__in=[lesson]).first()

	pls = ProfileLesson.objects.filter(profile=profile, lesson__in=course.lessons.all())
	cont = 0

	l = course.lessons.get(first=True)

	while cont < len(course.lessons.all()):
		if l == lesson:
			return True 
		else:
			p = pls.filter(lesson=l).first()
			if p:
				if p.completed:
					l = course.lessons.get(id=l.next_lesson)
					cont += 1
				else:
					return False
			else:
				return False
	return False

class Login(APIView):
	permission_classes = (AllowAny,)

	def post(self, request):
		"""
		Permite a los usuarios validar su identidad ante el sistema.
		"""
		try:
			username = request.data.get('username')
			password = request.data.get('password')

			Profile.objects.get(user__username=username)
			user = authenticate(username=username, password=password)

			if user is not None:
				try:
					token = Token.objects.get(user=user)
				except Token.DoesNotExist:
					token = Token.objects.create(user=user)

				return Response({"token": token.key})
			else:
				return Response(status=400)

		except Profile.DoesNotExist:
			return Response(status=400)

		except Exception as e:
			print(e)
			return Response(status=500)

class QuestionCRUD(APIView):
	permission_classes = (IsAuthenticated,)
	@method_decorator(user_passes_test(lambda u: u.has_perm("Cursos.maestro")))
	def get(self, request):
		try:
			id_question = request.GET.get("id", None)
			if id_question:
				quest = Question.objects.get(id=int(id_question))
				options = json.loads(quest.options)
				q = dict()
				q["id"] = quest.id
				q["text"] = quest.question_text
				q["options"] = options
				return Response(q, status=200)
		except Question.DoesNotExist:
			print(e)
			return Response({'msg': 'Question does not exist'}, status=404)
		except Exception as e:
			print(e)
			return Response({'msg': 'Internal error'}, status=500)

	@method_decorator(user_passes_test(lambda u: u.has_perm("Cursos.maestro")))
	def post(self, request):
		try:
			id_lesson = request.data.get("id_lesson", None)
			data = dict()
			data["question_text"] = request.data.get("question_text", None)
			data["multiple"] = request.data.get("multiple", None)
			data["alls"] = request.data.get("allselected", None)
			data["score"] = request.data.get("score", None)
			data["options"] = request.data.get("options", None)
			if id_lesson:
				r = createQuestion(data)
				if r[0]:
					lesson = Lesson.objects.get(id=int(id_lesson))
					lesson.questions.add(r[1])
					lesson.save()
					return Response({'msg': 'Question saved!'}, status=200)
				else:
					return Response({'msg': 'Data not valid'}, status=400)
		except Lesson.DoesNotExist:
			return Response({'msg': 'Lesson not valid'}, status=400)
		except Exception as e:
			print(e)
			return Response({'msg': 'Internal error'}, status=500)

	@method_decorator(user_passes_test(lambda u: u.has_perm("Cursos.maestro")))
	def put(self, request):
		try:
			id_question = request.data.get("id_question", None)
			question_text = request.data.get("question_text", None)
			alls = request.data.get("allselected", None)
			score = request.data.get("score", None)
			options = request.data.get("options", None)

			if id_question:
				quest = Question.objects.get(id=id_question)
				if question_text:
					quest.question_text = question_text
				if alls:
					if int(alls) == 1:
						quest.allselected = True
					else:
						quest.allselected = False
				if score:
					quest.score = int(score)
				if options:
					try:
						optionscheck = json.loads(options)
						quest.options = options
					except Exception as e:
						return Response({'msg': 'JSON not valid'}, status=400)
				if active is not None:
					if int(active) == 1:
						quest.active = True
					else:
						quest.active = False
				quest.save()
				return Response({'msg': 'Question updated!'}, status=200)
			else:
				return Response({'msg': 'Question not selected'}, status=400)
		except Question.DoesNotExist:
			return Response({'msg': 'Question not selected'}, status=400)
		except Exception as e:
			print(e)
			return Response({'msg': 'Internal error'}, status=500)

	@method_decorator(user_passes_test(lambda u: u.has_perm("Cursos.maestro")))
	def delete(self, request):
		try:
			id_question = request.data.get("id_question", None)

			if id_question:
				with transaction.atomic():
					quest = Question.objects.get(id=int(id_question))
					lesson = Lesson.objects.filter(questions__in=[quest]).first()
					lesson.questions.remove(quest)
					lesson.save()

					quest.active = False
					quest.save()
					return Response({'msg': 'Question deleted'}, status=200)
		except Question.DoesNotExist:
			return Response({'msg': 'Question not found'}, status=404)
		except Exception as e:
			print(e)
			return Response({'msg': 'Internal error'}, status=500)

class LessonCRUD(APIView):
	permission_classes = (IsAuthenticated,)
	@method_decorator(user_passes_test(lambda u: u.has_perm("Cursos.maestro")))
	def get(self, request):
		try:
			id_lesson = request.GET.get("id", None)
			if id_lesson:
				lesson = Lesson.objects.get(id=int(id_lesson))
				l = dict()
				l["id"] = lesson.id
				l["name"] = lesson.name
				l["nquestions"] = len(lesson.questions.all())
				l["approvalscore"] = lesson.approval_score
				return Response(l, status=200)
		except Lesson.DoesNotExist:
			print(e)
			return Response({'msg': 'Lesson does not exist'}, status=404)
		except Exception as e:
			print(e)
			return Response({'msg': 'Internal error'}, status=500)

	@method_decorator(user_passes_test(lambda u: u.has_perm("Cursos.maestro")))
	def post(self, request):
		try:
			id_course = request.data.get("id_course", None)
			data = dict()
			data["name"] = request.data.get("name", None)
			data["approval_score"] = request.data.get("approval_score", None)
			data["prev_lesson"] = request.data.get("prev_lesson", None)
			data["questions"] = request.data.get("questions", None)
			if id_course:
				with transaction.atomic():
					r = createLesson(data)
					if r[0]:
						l = r[1]
						course = Course.objects.get(id=int(id_course))
						if not data["prev_lesson"]:
							fl = course.lessons.get(first=True)
							fl.first = False
							fl.prev_lesson = l.id
							fl.save()
							l.first = True
							l.next_lesson = fl.id
							l.save()
						course.lessons.add(l)
						course.save()
						return Response({'msg': 'Lesson saved!'}, status=200)
					else:
						return Response({'msg': 'Data not valid'}, status=400)
			else:
				return Response({'msg': 'Course not selected'}, status=400)
		except Exception as e:
			raise e
		return Response({'msg': 'Internal error'}, status=200)

	@method_decorator(user_passes_test(lambda u: u.has_perm("Cursos.maestro")))
	def put(self, request):
		try:
			id_lesson = request.data.get("id_lesson", None)
			name = request.data.get("name", None)
			approval_score = request.data.get("approval_score", None)
			if id_lesson:
				lesson = Lesson.objects.get(id=id_lesson)
				if name:
					lesson.name = name
				if approval_score:
					lesson.approval_score = approval_score
				lesson.save()
				return Response({'msg': 'Lesson updated!'}, status=200)
			else:
				return Response({'msg': 'Lesson not selected'}, status=400)
		except Exception as e:
			raise e
		return Response({'msg': 'Internal error'}, status=200)

	@method_decorator(user_passes_test(lambda u: u.has_perm("Cursos.maestro")))
	def delete(self, request):
		try:
			id_lesson = request.data.get("id_lesson", None)

			if id_lesson:
				with transaction.atomic():
					lesson = Lesson.objects.get(id=int(id_lesson))
					course = Course.objects.filter(lessons__in=[lesson]).first()

					course.lessons.remove(lesson)
					course.save()

					if lesson.next_lesson and lesson.prev_lesson:
						print("n,p")
						n = course.lessons.get(id=lesson.next_lesson)
						p = course.lessons.get(id=lesson.prev_lesson)

						p.next_lesson = n.id
						n.prev_lesson = p.id

						p.save()
						n.save()
					elif lesson.next_lesson:
						print("n")
						n = course.lessons.get(id=lesson.next_lesson)
						n.first = True
						n.prev_lesson = None
						n.save()
					else:
						print("p")
						p = course.lessons.get(id=lesson.prev_lesson)
						p.next_lesson = None
						p.save()

					for i in lesson.questions.all():
						i.active = False
						i.save()

					lesson.active = False
					lesson.save()
					return Response({'msg': 'Lesson deleted'}, status=200)
			else:
				return Response({'msg': 'Incomplete data'}, status=400)
		except Lesson.DoesNotExist:
			return Response({'msg': 'Lesson not found'}, status=404)
		except Exception as e:
			print(e)
			return Response({'msg': 'Internal error'}, status=500)

class CourseCRUD(APIView):
	permission_classes = (IsAuthenticated,)
	@method_decorator(user_passes_test(lambda u: u.has_perm("Cursos.maestro")))
	def get(self, request):
		try:
			id_course = request.GET.get("id", None)
			if id_course:
				course = Course.objects.get(id=int(id_course))
				l = dict()
				l["id"] = course.id
				l["name"] = course.name
				l["nlessons"] = len(course.lessons.all())
				return Response(l, status=200)
		except Course.DoesNotExist:
			print(e)
			return Response({'msg': 'Course does not exist'}, status=404)
		except Exception as e:
			print(e)
			return Response({'msg': 'Internal error'}, status=500)

	@method_decorator(user_passes_test(lambda u: u.has_perm("Cursos.maestro")))
	def post(self, request):
		try:
			data = dict()
			name = request.data.get("name", None)
			prev_course = request.data.get("prev_course", None)
			lessons = request.data.get("lessons", None)
			cont = 0
			if name and lessons:
				with transaction.atomic():
					c = Course.objects.create(
						name=name,
						)
					if prev_course:
						pc = Course.objects.get(id=prev_course)
						c.next_course = pc.next_course
						pc.next_course = c.id
						pc.save()
					else:
						fc = Course.objects.filter(first=True).first()
						if fc:
							fc.first = False
							fc.prev_course = c.id
							fc.save()
							c.first = True
							c.next_course = fc.id
						else:
							c.first = True
					for i in lessons:
						r = createLesson(i)
						if r[0]:
							if cont == 0:
								r[1].first = True
								r[1].save()
								prev = r[1]
							else:
								prev.next_lesson = r[1].id
								prev.save()
								prev = r[1]
							c.lessons.add(r[1])
							cont += 1
						else:
							pass
					c.save()
					return Response({'msg': 'Course saved!'}, status=200)
		except Exception as e:
			raise e
		return Response({'msg': 'Internal error'}, status=200)

	@method_decorator(user_passes_test(lambda u: u.has_perm("Cursos.maestro")))
	def put(self, request):
		try:
			id_course = request.data.get("id_course", None)
			name = request.data.get("name", None)
			if id_course:
				course = Course.objects.get(id=id_course)
				if name:
					course.name = name
				course.save()
				return Response({'msg': 'Course updated!'}, status=200)
			else:
				return Response({'msg': 'Course not selected'}, status=400)
		except Exception as e:
			raise e
		return Response({'msg': 'Internal error'}, status=200)

	@method_decorator(user_passes_test(lambda u: u.has_perm("Cursos.maestro")))
	def delete(self, request):
		try:
			id_course = request.data.get("id_course", None)

			if id_course:
				with transaction.atomic():
					course = Course.objects.get(id=int(id_course))

					if course.first:
						if course.next_course:
							ncourse = Course.objects.get(id=course.next_course)
							ncourse.first = True
							ncourse.save()
						course.first=False

					for i in course.lessons.all():
						for j in i.questions.all():
							j.active = False
							j.save()
						i.active = False
						i.save()

					course.active = False
					course.save()
					return Response({'msg': 'Course deleted'}, status=200)
			else:
				return Response({'msg': 'Course not selected'}, status=400)
		except Course.DoesNotExist:
			return Response({'msg': 'Course not found'}, status=404)
		except Exception as e:
			print(e)
			return Response({'msg': 'Internal error'}, status=500)

class ListCourse(APIView):
	permission_classes = (IsAuthenticated,)

	#2-Completed, 1-Pending, 0-Not Available
	def get(self, request):
		try:
			profile = Profile.objects.get(user=request.user)

			if profile:
				cs = list()
				can = True
				checked = []
				courses = Course.objects.filter(active=True)
				completed = profile.completed_courses.all()

				first = courses.get(first=True)
				c = dict()
				c["id"] = first.id
				c["name"] = first.name
				if first in completed:
					c["status"] = 2
					c["status_text"] = "Completed"
				else:
					c["status"] = 1
					c["status_text"] = "Pending"
					can = False
				cs.append(c)
				checked.append(first)
				act = first
				print(len(checked))
				print(len(courses))

				while len(checked) < len(courses):
					act = courses.get(id=act.next_course)
					c = dict()
					c["id"] = act.id
					c["name"] = act.name
					if act in completed:
						c["status"] = 2
						c["status_text"] = "Completed"
					elif act not in completed and can:
						c["status"] = 1
						c["status_text"] = "Pending"
						can = False
					else:
						c["status"] = 0
						c["status_text"] = "Not available"
					cs.append(c)
					checked.append(act)

				r = {"Courses":cs}
				return Response(r, status=200)
			else:
				return Response({'msg': 'User not registered'}, status=400)
		except Exception as e:
			print(e)
			return Response({'msg': 'Internal error'}, status=500)

class ListLessons(APIView):
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		try:
			id_course = request.GET.get("id", None)
			profile = Profile.objects.get(user=request.user)

			if profile and id_course:
				ls = list()
				can = True
				checked = []
				courses = Course.objects.get(id=int(id_course))

				first = courses.lessons.get(first=True)
				pl = ProfileLesson.objects.filter(profile=profile, lesson=first).first()

				if pl:
					l = dict()
					l["id"] = first.id
					l["name"] = first.name
					if pl.completed:
						l["status"] = 2
					else:
						l["status"] = 1
						can = False
					ls.append(l)
					checked.append(first)
					act = first
				else:
					pl = ProfileLesson.objects.create(
						profile = profile,
						lesson = first
						)
					l = dict()
					l["id"] = first.id
					l["name"] = first.name
					l["status"] = 1
					can = False
					ls.append(l)
					checked.append(first)
					act = first

				while len(checked) < len(courses.lessons.all()):
					act = courses.lessons.get(id=act.next_lesson)
					if can:
						pl = ProfileLesson.objects.filter(profile=profile, lesson=act).first()

						if pl:
							l = dict()
							l["id"] = act.id
							l["name"] = act.name
							if pl.completed:
								l["status"] = 2
							else:
								l["status"] = 1
								can = False
							ls.append(l)
							checked.append(act)
						else:
							pl = ProfileLesson.objects.create(
								profile = profile,
								lesson = act
								)
							l = dict()
							l["id"] = act.id
							l["name"] = act.name
							l["status"] = 1
							can = False
							ls.append(l)
							checked.append(act)
					else:
						l = dict()
						l["id"] = act.id
						l["name"] = act.name
						l["status"] = 0
						ls.append(l)
						checked.append(act)

				r = {"Lessons":ls}
				return Response(r, status=200)
			else:
				return Response({'msg': 'User not registered'}, status=400)
		except Exception as e:
			print(e)
			return Response({'msg': 'Internal error'}, status=500)

class QuestionDetails(APIView):
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		try:
			id_lesson = request.GET.get("id", None)
			profile = Profile.objects.get(user=request.user)

			if id_lesson:
				qs = list()
				lesson = Lesson.objects.get(id=int(id_lesson))

				la = checkLessonAvailability(lesson, profile)

				if not la:
					return Response({"msg": "You can't try this lesson until you end all the previous ones"}, status=400)

				pl = ProfileLesson.objects.filter(profile=profile, lesson=lesson).first()
				if pl:
					pass
				else:
					pl = ProfileLesson.objects.create(
						profile = profile,
						lesson = lesson
						)

				for i in lesson.questions.all():
					q = dict()
					q["text"] = i.question_text
					q["id"] = i.id
					if i.multiple:
						q["multiple"] = True
						if i.allselected:
							q["all"] = True
						else:
							q["all"] = False
					else:
						q["multiple"] = False

					options = json.loads(i.options)
					q["options"] = list()
					for j in options:
						print(j)
						o = dict()
						o["text"] = j["text"]
						o["letra"] = j["letra"]
						q["options"].append(o)

					qs.append(q)

				r = {"questions":qs}

				return Response(r, status=200)
			else:
				return Response({"msg": "Lesson not selected"}, status=400)
		except Exception as e:
			print(e)
			return Response({'msg': 'Internal error'}, status=500)

	"""
	{
		"id_lesson": 5,
		"answers":[
			{
				"id": 10,
				"answer": ["A"]
			},
			{
				"id": 11,
				"answer": ["A", "B"]
			}
		]
	}
	"""
	def post(self, request):
		try:
			id_lesson = request.data.get("id_lesson", None)
			answers = request.data.get("answers", None)
			answers = build_dict(answers, key="id")
			profile = Profile.objects.get(user=request.user)

			total_score = 0

			if id_lesson and answers:
				with transaction.atomic():
					lesson = Lesson.objects.get(id=int(id_lesson))

					la = checkLessonAvailability(lesson, profile)

					if not la:
						return Response({"msg": "You can't try this lesson until you end all the previous ones"}, status=400)

					if not len(answers) == len(lesson.questions.all()):
						return Response({"msg":"Not all questions were sended!"}, status=400)

					pl = ProfileLesson.objects.filter(profile=profile, lesson=lesson).first()

					for i in lesson.questions.all():
						options = json.loads(i.options)
						ops = build_dict(options, key="letra")

						ans = answers[i.id]["answer"]

						if i.multiple:
							allright = True
							cright = 0
							a = pl.answers.filter(question__id=i.id).first()
							if a:
								a.answer = json.dumps(ops)
								a.save()
							else:
								a = Answer.objects.create(
									question=i,
									answer= json.dumps(ops),
									)

							for j in ans:
								if ops[j]["correct"] == 0:
									allright = False
								else:
									cright += 1
							if i.allselected and allright:
								counter = 0
								for h in ops:
									if ops[h]["correct"] == 1:
										counter += 1
								if cright == counter:
									a.correct = True
									a.save()
									total_score += i.score
								else:
									a.correct = False
									a.save()
							else:
								if allright:
									a.correct = True
									a.save()
									total_score += i.score
								else:
									a.correct = False
									a.save()
						else:
							a = pl.answers.filter(question__id=i.id).first()
							if a:
								a.answer = json.dumps(ops[ans[0]])
								a.save()
							else:
								a = Answer.objects.create(
									question=i,
									answer= json.dumps(ops[ans[0]]),
									)
							if ops[ans[0]]["correct"] == 1:
								a.correct = True
								a.save()
								total_score += i.score
							else:
								a.correct = False
								a.save()
					if total_score >= lesson.approval_score:
						pl.completed = True
						pl.save()
						comp = checkCourse(lesson, profile)
						if comp:
							return Response({"msg":"Lesson Approved! Course Completed"}, status=200)
						else:
							return Response({"msg":"Lesson Approved!"}, status=200)
					else:
						return Response({"msg": "Lesson Failed!"}, status=200)
			else:
				return Response({"msg": "Data incomplete"}, status=400)
		except Exception as e:
			print(e)
			return Response({'msg': 'Internal error'}, status=500)
