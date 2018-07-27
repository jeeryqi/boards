from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory, modelform_factory
from django.db.models import Count
from django.utils import timezone
from django.utils.decorators import method_decorator

from .forms import NewTopicForm, PostForm
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
    paginate_by = 3

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('board_id'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = self.board
        return context


class PostListView(generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'boards/topic_posts.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('board_id'), pk=self.kwargs.get('topic_id'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


@method_decorator(login_required, name='dispatch')
class PostUpdateView(generic.UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'boards/edit_post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('boards:topic_posts', board_id=post.topic.board.pk, topic_id=post.topic.pk)


# ModelFormSet写法
def new_topic_formset(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    newtopicformset = modelformset_factory(Topic, form=NewTopicForm, fields=('subject', 'message'))
    if request.method == 'POST':
        formset = newtopicformset(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    user = User.objects.first()
                    topic = form.save(commit=False)
                    topic.board = board
                    topic.starter = user
                    topic.save()
                    Post.objects.create(
                        message=form.cleaned_data.get('message'),
                        topic=topic,
                        created_by=user
                    )
            return redirect('boards:topic', board_id=board_id)
    else:
        formset = newtopicformset(queryset=Topic.objects.none())

    return render(request, 'boards/new_topic.html', {'board': board, 'form': formset})


# ModelFormfactory写法
def new_topic_form_factory(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    newtopicform = modelform_factory(Topic, form=NewTopicForm, fields=('subject', 'message'))
    if request.method == 'POST':
        form = newtopicform(request.POST)
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
        form = newtopicform()
    return render(request, 'boards/new_topic.html', {'board': board, 'form': form})


# ModelForm写法
@login_required
def new_topic_form(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    # newtopicform = modelform_factory(Topic, form=NewTopicForm, fields=('subject', 'message'))
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            # user = User.objects.first()  # TODO: get the currently logged in user
            user = request.user
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            # return redirect('boards:topic', board_id=board_id)  # TODO: redirect to the created topic page
            return redirect('boards:topic_posts', board_id=board_id,
                            topic_id=topic.id)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'boards/new_topic.html', {'board': board, 'form': form})


@login_required
def topic_posts(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board_id=board_id, pk=topic_id)
    topic.views += 1
    topic.save()
    return render(request, 'boards/topic_posts.html', {'topic': topic})


@login_required
def reply_topic(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board_id=board_id, pk=topic_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = post.created_at  # timezone.now()
            topic.save()
            return redirect('boards:topic_posts', board_id=board_id, topic_id=topic_id)
    else:
        form = PostForm()
    return render(request, 'boards/reply_topic.html', {'topic': topic, 'form': form})
