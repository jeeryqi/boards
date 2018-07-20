from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.contrib.auth.models import User
from django.forms import modelformset_factory, modelform_factory

from .forms import NewTopicForm
from .models import Board, Topic, Post


# Create your views here.
class HomeListView(generic.ListView):
    model = Board
    template_name = 'boards/home.html'
    context_object_name = 'all_boards_list'

    # def get_queryset(self):
    #     return Board.objects.all()


class TopicListView(generic.ListView):
    model = Topic
    context_object_name = 'topics_by_board_list'
    template_name = 'boards/topics.html'

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('board_id'))
        queryset = self.board.topics.order_by('-last_updated')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = self.board
        return context

# ModelFormSet写法
def new_topic_formset(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    NewTopicFormSet = modelformset_factory(Topic, form=NewTopicForm, fields=('subject', 'message'))
    if request.method == 'POST':
        # return HttpResponse(board.name)
        formset = NewTopicFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    user = User.objects.first()
                    topic = form.save(commit=False)
                    topic.board = board
                    topic.starter = user
                    topic.save()
                    Post.objects.create(
                        message = form.cleaned_data.get('message'),
                        topic = topic,
                        created_by = user
                    )
            return redirect('boards:topic', board_id=board_id)
    else:
        formset = NewTopicFormSet(queryset=Topic.objects.none())

    return render(request, 'boards/new_topic.html', {'board': board, 'form': formset})

# ModelForm写法
def new_topic_form(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    NewTopicFormForm = modelform_factory(Topic, form=NewTopicForm, fields=('subject', 'message'))
    if request.method == 'POST':
        form = NewTopicFormForm(request.POST)
        if form.is_valid():
            user = User.objects.first()  # TODO: get the currently logged in user
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
        return redirect('boards:topic', board_id=board_id)  # TODO: redirect to the created topic page
    else:
        form = NewTopicFormForm(request.GET)
    return render(request, 'boards/new_topic.html', {'board': board, 'form': form})
