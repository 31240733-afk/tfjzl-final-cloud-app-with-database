from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Question, Choice, Submission


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(
        request,
        'course/course_details_bootstrap.html',
        {'course': course}
    )

def exam(request, lesson_id):
    questions = Question.objects.filter(lesson_id=lesson_id)

    return render(
        request,
        'course/exam.html',
        {
            'lesson': questions.first().lesson,
            'questions': questions,
        }
    )

def submit(request, lesson_id):
    if request.method == 'POST':
        questions = Question.objects.filter(lesson_id=lesson_id)
        score = 0

        for question in questions:
            selected_id = request.POST.get(f'question_{question.id}')

            if selected_id:
                choice = get_object_or_404(Choice, id=selected_id)

                is_correct = choice.is_correct

                Submission.objects.create(
                    question=question,
                    selected_choice=choice,
                    is_correct=is_correct
                )

                if is_correct:
                    score += 1

        return redirect('show_exam_result', lesson_id=lesson_id, score=score)

    return redirect('course_details', course_id=1)


def show_exam_result(request, lesson_id, score):
    questions = Question.objects.filter(lesson_id=lesson_id)

    submissions = Submission.objects.filter(
        question__in=questions
    ).order_by('id')

    return render(
        request,
        'course/exam_result.html',
        {
            'lesson': questions.first().lesson if questions.exists() else None,
            'questions': questions,
            'submissions': submissions,
            'score': score,
            'total': questions.count(),
        }
    )