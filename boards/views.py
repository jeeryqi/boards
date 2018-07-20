from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.contrib.auth.models import User

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

def new_topic(request, board_id):
    board = get_object_or_404(Board, pk=board_id)

    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']

        user = User.objects.first()

        topic = Topic.objects.create(
            subject = subject,
            board = board,
            starter = user
        )

        post = Post.objects.create(
            message = message,
            topic = topic,
            created_by = user
        )

        return redirect('boards:topic', pk=board_id)

    return render(request, 'boards/new_topic.html', {'board': board})