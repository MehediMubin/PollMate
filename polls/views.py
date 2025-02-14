from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.db.models import F
from django.views import generic

# Create your views here.
class IndexView(generic.ListView):
   template_name = 'polls/index.html'
   context_object_name = "latest_question_list"
   
   def get_queryset(self):
      return Question.objects.order_by('pub_date') 

# def index(request):
#    latest_question_list = Question.objects.order_by('pub_date')
#    return render(request, 'polls/index.html', {"latest_question_list": latest_question_list})

class DetailView(generic.DetailView):
   model = Question
   template_name = 'polls/detail.html'

# def detail(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls/detail.html', {"question": question})

class ResultsView(generic.DetailView):
   model = Question
   template_name = 'polls/results.html'

# def results(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls/results.html', {"question": question})


def vote(request, question_id):
   question = get_object_or_404(Question, pk=question_id)
   try:
      selected_choice = question.choice_set.get(pk=request.POST['choice'])
   except (KeyError, Choice.DoesNotExist):
      return render(request, 'polls/detail.html', {
         "question": question,
         "error_message": "You didn't select a choice"
      })
   else:
      selected_choice.votes = F("votes") + 1
      selected_choice.save()
      return redirect('polls:results', pk=question.id)