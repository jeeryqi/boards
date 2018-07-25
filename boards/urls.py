from django.urls import path
from . import views

app_name = 'boards'
urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    path('<int:board_id>/', views.TopicListView.as_view(), name='topic'),
    path('<int:board_id>/new/', views.new_topic_form, name='new_topic'),
    path('<int:board_id>/topics/<int:topic_id>/', views.topic_posts, name='topic_posts'),
    path('<int:board_id>/topics/<int:topic_id>/reply/', views.reply_topic, name='reply_topic'),
]