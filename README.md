## Installation instructions
The API was developed using Python 3.7.1

```bash
virtualenv pruebadacodes
source pruebadacodes/bin/activate
cd E-Learning/
pip install -r requitements.txt
python manage.py migrate
python manage.py runserver
```
### Usage

In order to use the API, is necessary to create a Token for both, the teacher and the student, and use the right one, depending on the task. If using the included SQLite DB, the default users are:

Student:
- username: alumno@example.com
- password: passworddacodes

Teacher: 
- username: maestro@example.com
- password: pruebadacodes

And just in case, the admin account:
- username: admin
- password: pruebadacode

A POST Request must be done to /api/login/ to retrieve the Token

```
POST /api/login/

{
    "username":"alumno@example.com",
    "password":"passworddacodes"
} 

Response

{
    "token": "b47a4f78a2454d9e14890a436b8d32151c81f0b1"
}
```

From this point, all calls to the API must include the Token in the authorization header as authentication on the platform. An Example Python file with request functions was added to the project folder for easiness of testing, requires installation of Requests library.

**Endpoints available:**

```
CRUD Course (Teacher)

GET /api/courses/?id=<ID>
POST /api/courses/
PUT /api/courses/
DELETE /api/courses/

CRUD Lessons (Teacher)

GET /api/lessons/?id=<ID>
POST /api/lessons/
PUT /api/lessons/
DELETE /api/lessons/

CRUD Questions (Teacher)

GET /api/questions/?id=<ID>
POST /api/questions/
PUT /api/questions/
DELETE /api/questions/

Student's Endpoints (Student)
GET /api/get_courses/
GET /api/get_lessons/?id=<ID_Course>
GET /api/question_details/?id=<ID_Lesson>
POST /api/question_details/
```

### Technologies Used

**Django:** Python Web Framework, used to create Backend on Python. \
**SQLite:** Default Database included with Django, doesn't require installation. \
**Django RestFramework** Django Library that integrates tools for the implementation of a RESTful API and enables the use of Token authentication.
