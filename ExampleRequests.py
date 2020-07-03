import requests
import json
import time

name = "http://localhost:8000"

#token = "5b1881c1a55fa01e548ff3aca37a5c6019064a63" #Maestro
token = "b47a4f78a2454d9e14890a436b8d32151c81f0b1" #Alumno

# Login
def testGetToken():
	header = {'content-type':'application/json'}

	body = {
		"username":"alumno@example.com",
		"password":"passworddacodes"
	}

	url = name + '/api/login/'

	r = requests.post(url, data= json.dumps(body), headers=header)
	res = json.loads(r.content)
	print(r.request.body)
	print(r.request.headers)
	print("")
	print(json.dumps(res, indent=4, sort_keys=True))

# CRUD Cursos
def testGetCurso():
	header = {'content-type':'application/json', 'authorization': 'Token ' + token}

	url = name + '/api/courses/?id=1'

	r = requests.get(url, headers=header)
	res = json.loads(r.content)
	print("")
	print(json.dumps(res, indent=4, sort_keys=True))

def testPostCurso():
	header = {'content-type':'application/json', 'authorization': 'Token ' + token}

	dato = {
	"name": "Curso 1",
	"lessons": [
		{
			"name":"Lesson 1",
			"approval_score": 100,
			"questions":[
				{
					"multiple": 0,
					"question_text": "What is something?",
					"score": 50,
					"alls": 0,
					"options": [
						{"letra":"A", "text":"Algo", "correct":1},
						{"letra":"B", "text":"Algo2", "correct":0}
					]
				},
				{
					"multiple": 1,
					"question_text": "What is something?",
					"score": 50,
					"alls": 0,
					"options": [
						{"letra":"A", "text":"Algo", "correct":1},
						{"letra":"B", "text":"Algo2", "correct":0},
						{"letra":"C", "text":"Algo3", "correct":1}
					]
				}
			]
		},
		{
			"name":"Lesson 2",
			"approval_score": 100,
			"questions":[
				{
					"multiple": 0,
					"question_text": "What is something?",
					"score": 50,
					"alls": 0,
					"options": [
						{"letra":"A", "text":"Algo", "correct":1},
						{"letra":"B", "text":"Algo2", "correct":0}
					]
				},
				{
					"multiple": 1,
					"question_text": "What is something?",
					"score": 50,
					"alls": 0,
					"options": [
						{"letra":"A", "text":"Algo", "correct":1},
						{"letra":"B", "text":"Algo2", "correct":0},
						{"letra":"C", "text":"Algo3", "correct":1}
					]
				}
			]
		}
	]
	}

	url = name + '/api/courses/'

	r = requests.post(url, data = json.dumps(dato), headers=header)
	res = json.loads(r.content)
	print("")
	print(json.dumps(res, indent=4, sort_keys=True))

def testPutCurso():
	header = {'content-type':'application/json', 'authorization': 'Token ' + token}

	url = name + '/api/courses/'

	dato = {
			"id_course":1,
			"name": "Curso Principal",
		}

	r = requests.put(url, data = json.dumps(dato), headers=header)
	res = json.loads(r.content)
	print("")
	print(json.dumps(res, indent=4, sort_keys=True))

def testDeleteCurso():
	header = {'content-type':'application/json', 'authorization': 'Token ' + token}

	url = name + '/api/courses/'

	dato = {
			"id_course":1
		}

	r = requests.delete(url, data = json.dumps(dato), headers=header)
	res = json.loads(r.content)
	print("")
	print(json.dumps(res, indent=4, sort_keys=True))

# CRUD Lesson
def testGetLesson():
	header = {'content-type':'application/json', 'authorization': 'Token ' + token}

	url = name + '/api/lessons/?id=2'

	r = requests.get(url, headers=header)
	res = json.loads(r.content)
	print("")
	print(json.dumps(res, indent=4, sort_keys=True))

def testPostLesson():
	header = {'content-type':'application/json', 'authorization': 'Token ' + token}

	dato = {
			"name":"Lesson 3",
			"approval_score": 100,
			"prev_lesson":1,
			"id_course":1,
			"questions":[
				{
					"multiple": 0,
					"question_text": "What is something?",
					"score": 50,
					"alls": 0,
					"options": [
						{"letra":"A", "text":"Algo", "correct":1},
						{"letra":"B", "text":"Algo2", "correct":0}
					]
				},
				{
					"multiple": 1,
					"question_text": "What is something?",
					"score": 50,
					"alls": 0,
					"options": [
						{"letra":"A", "text":"Algo", "correct":1},
						{"letra":"B", "text":"Algo2", "correct":0},
						{"letra":"C", "text":"Algo3", "correct":1}
					]
				}
			]
		}

	url = name + '/api/lessons/'

	r = requests.post(url, data = json.dumps(dato), headers=header)
	res = json.loads(r.content)
	print("")
	print(json.dumps(res, indent=4, sort_keys=True))

def testPutLesson():
	header = {'content-type':'application/json', 'authorization': 'Token ' + token}

	url = name + '/api/lessons/'

	dato = {
			"id_lesson":2,
			"approval_score": 75,
		}

	r = requests.put(url, data = json.dumps(dato), headers=header)
	res = json.loads(r.content)
	print("")
	print(json.dumps(res, indent=4, sort_keys=True))

def testDeleteLesson():
	header = {'content-type':'application/json', 'authorization': 'Token ' + token}

	url = name + '/api/lessons/'

	dato = {
			"id_lesson":4
		}

	r = requests.delete(url, data = json.dumps(dato), headers=header)
	res = json.loads(r.content)
	print("")
	print(json.dumps(res, indent=4, sort_keys=True))

# CRUD Question
def testGetQuestion():
	header = {'content-type':'application/json', 'authorization': 'Token ' + token}

	url = name + '/api/questions/?id=7'

	r = requests.get(url, headers=header)
	res = json.loads(r.content)
	print("")
	print(json.dumps(res, indent=4, sort_keys=True))

def testPostQuestion():
	header = {'content-type':'application/json', 'authorization': 'Token ' + token}

	dato = {
			"id_lesson":1,
			"multiple": 0,
			"question_text": "What is something added?",
			"score": 50,
			"alls": 0,
			"options": [
				{"letra":"A", "text":"Algo", "correct":1},
				{"letra":"B", "text":"Algo2", "correct":0}
			]
		}

	url = name + '/api/questions/'

	r = requests.post(url, data = json.dumps(dato), headers=header)
	res = json.loads(r.content)
	print("")
	print(json.dumps(res, indent=4, sort_keys=True))

def testPutQuestion():
	header = {'content-type':'application/json', 'authorization': 'Token ' + token}

	url = name + '/api/questions/'

	dato = {
			"id_question":7,
			"question_text": "What is something modified?",
			"score": 50,
			"active": 0,
		}

	r = requests.put(url, data = json.dumps(dato), headers=header)
	res = json.loads(r.content)
	print("")
	print(json.dumps(res, indent=4, sort_keys=True))

def testDeleteQuestion():
	header = {'content-type':'application/json', 'authorization': 'Token ' + token}

	url = name + '/api/questions/'

	dato = {
			"id_question":6,
		}

	r = requests.delete(url, data = json.dumps(dato), headers=header)
	res = json.loads(r.content)
	print("")
	print(json.dumps(res, indent=4, sort_keys=True))

# Requested Endpoints
def testGetListCourses():
	header = {'content-type':'application/json', 'authorization': 'Token ' + token}

	url = name + '/api/get_courses/'

	r = requests.get(url, headers=header)
	res = json.loads(r.content)
	print("")
	print(json.dumps(res, indent=4, sort_keys=True))

def testGetListLessons():
	header = {'content-type':'application/json', 'authorization': 'Token ' + token}

	url = name + '/api/get_lessons/?id=4'

	r = requests.get(url, headers=header)
	res = json.loads(r.content)
	print("")
	print(json.dumps(res, indent=4, sort_keys=True))

def testGetQuestionDetails():
	header = {'content-type':'application/json', 'authorization': 'Token ' + token}

	url = name + '/api/question_details/?id=10'

	r = requests.get(url, headers=header)
	res = json.loads(r.content)
	print("")
	print(json.dumps(res, indent=4, sort_keys=True))

def testPostQuestionDetails():
	header = {'content-type':'application/json', 'authorization': 'Token ' + token}

	dato =  {
		"id_lesson": 10,
		"answers":[
			{
				"id": 20,
				"answer": ["A"]
			},
			{
				"id": 21,
				"answer": ["A", "C"]
			}
		]
	}

	url = name + '/api/question_details/'

	r = requests.post(url, data = json.dumps(dato), headers=header)
	res = json.loads(r.content)
	print("")
	print(json.dumps(res, indent=4, sort_keys=True))