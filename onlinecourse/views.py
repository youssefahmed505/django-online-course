from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Question, Submission, Choice

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        selected_choice_ids = request.POST.getlist('choice')
        
        # بنعمل Submission جديد
        submission = Submission.objects.create(enrollment_id=1) 
        
        for choice_id in selected_choice_ids:
            submission.choices.add(choice_id)
        submission.save()
        
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    total_score = 0
    selected_choices = submission.choices.all()
    selected_choice_ids = [choice.id for choice in selected_choices]
    
    for question in course.question_set.all():
        if question.is_get_score(selected_choice_ids):
            total_score += question.grade
            
    context = {
        'course': course,
        'submission': submission,
        'total_score': total_score
    }
    return render(request, 'onlinecourse/course_details_bootstrap.html', context)
