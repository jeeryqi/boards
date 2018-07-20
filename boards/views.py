from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.views import generic

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
    return render(request, 'boards/new_topic.html', {'board': board})