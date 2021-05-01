from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Question, Choice
from django.http import JsonResponse

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

# Get questions and display them
# @login_required
def index(request):
    current_questions = Question.objects.order_by('-pub_date')[:5]
    context = {'current_questions': current_questions}
    return render(request, 'polls/index.html', context)

# Show specific question and choices
@login_required
def detail(request, question_id):
  try:
    question = Question.objects.get(pk=question_id)
  except Question.DoesNotExist:
    messages.warning(request, "Poll does not exist")
    return HttpResponseRedirect(reverse('index'))
  return render(request, 'polls/detail.html', { 'question': question })

# Get question and display results
# @login_required
def results(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'polls/results.html', { 'question': question })

# Vote for a question choice
@login_required
def vote(request, question_id):
    # print(request.POST['choice'])
    user = User.objects.get(pk=request.user.pk)
    if user.hasVoted != True:
      question = get_object_or_404(Question, pk=question_id)
      try:
          selected_choice = question.choice_set.get(pk=request.POST['choice'])
      except (KeyError, Choice.DoesNotExist):
          # Redisplay the question voting form.
          return render(request, 'polls/detail.html', {
              'question': question,
              'error_message': "You didn't select an aspirant.",
          })

      else:
        selected_choice.votes += 1
        selected_choice.save()
        user.hasVoted = True
        user.save()
        messages.success(request, 'Voting Successfull')
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        
    else:
      messages.warning(request, 'You have already voted')
      return HttpResponseRedirect(reverse('index'))
@login_required
def resultsData(request, obj):
    votedata = []

    question = Question.objects.get(id=obj)
    votes = question.choice_set.all()

    for i in votes:
        votedata.append({i.choice_text:i.votes})

    return JsonResponse(votedata, safe=False)
