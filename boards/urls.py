from django.urls import path
from . import views

app_name = 'boards'
urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    path('<int:board_id>/', views.TopicListView.as_view(), name='topic'),
    path('<int:board_id>/new/', views.new_topic_form, name='new_topic'),
]