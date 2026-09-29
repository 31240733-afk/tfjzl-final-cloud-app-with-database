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

    lesson = questions.first().lesson if questions.exists() else None

    return render(
        request,
        'course/exam.html',
        {
            'lesson': lesson,
            'questions': questions,
        }
    )


def submit(request, lesson_id):
    if request.method == 'POST':
        questions = Question.objects.filter(lesson_id=lesson_id)
        score = 0
        first_submission_id = None

        for question in questions:
            selected_id = request.POST.get(
                f'question_{question.id}'
            )

            if selected_id:
                choice = get_object_or_404(
                    Choice,
                    id=selected_id
                )

                is_correct = choice.is_correct

                submission = Submission.objects.create(
                    question=question,
                    selected_choice=choice,
                    is_correct=is_correct
                )

                if first_submission_id is None:
                    first_submission_id = submission.id

                if is_correct:
                    score += 1

        course = questions.first().lesson.course

        return redirect(
            'show_exam_result',
            course_id=course.id,
            submission_id=first_submission_id
        )

    return redirect('course_details', course_id=1)


def show_exam_result(request, course_id, submission_id):
    submission = get_object_or_404(
        Submission,
        id=submission_id
    )

    lesson = submission.question.lesson
    questions = Question.objects.filter(
        lesson=lesson
    )

    submissions = Submission.objects.filter(
        question__in=questions
    ).order_by('id')

    score = submissions.filter(
        is_correct=True
    ).count()

    return render(
        request,
        'course/exam_result.html',
        {
            'lesson': lesson,
            'questions': questions,
            'submissions': submissions,
            'score': score,
            'total': questions.count(),
        }
    )