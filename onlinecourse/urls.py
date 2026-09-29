from django.contrib import admin
from django.urls import path
from course import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'course/<int:course_id>/',
        views.course_details,
        name='course_details'
    ),

    path(
        'exam/<int:lesson_id>/',
        views.exam,
        name='exam'
    ),

    path(
        'submit/<int:lesson_id>/',
        views.submit,
        name='submit'
    ),

    path(
        'exam-result/<int:lesson_id>/<int:score>/',
        views.show_exam_result,
        name='show_exam_result'
    ),
]