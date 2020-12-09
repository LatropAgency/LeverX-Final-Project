from django.urls import path, include

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)
router.register('lectures', views.LectureViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('courses/<int:pk>/participant', views.ParticipantView.as_view()),
    path('courses/<int:pk>/lecture', views.AvaibleLectureListView.as_view()),
    path('tasks/<int:pk>/solution', views.CompletedSolutionListView.as_view()),
    path('lectures/<int:pk>/task', views.AvaibleTaskListView.as_view()),
    path('solutions/<int:pk>/mark', views.SolutionMarkView.as_view()),
    path('tasks/', views.TaskView.as_view()),
    path('solutions/', views.SolutionView.as_view()),
    path('marks/<int:pk>/', views.MarkView.as_view()),
    path('marks/', views.MarkView.as_view()),
    path('comments/', views.CommentView.as_view()),
    path('marks/<int:pk>/comment', views.CommentView.as_view()),
    path('users/', views.UserList.as_view()),
]
