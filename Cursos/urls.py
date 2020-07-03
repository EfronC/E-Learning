from django.urls import path

from .views import *

from rest_framework.authtoken import views

app_name = 'api'




urlpatterns = [
    path('login/', Login.as_view()),
    path('courses/', CourseCRUD.as_view()),
    path('lessons/', LessonCRUD.as_view()),
    path('questions/', QuestionCRUD.as_view()),
    path('get_courses/', ListCourse.as_view()),
    path('get_lessons/', ListLessons.as_view()),
    path('question_details/', QuestionDetails.as_view()),

]
