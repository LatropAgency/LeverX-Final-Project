from django.urls import path, include

from rest_framework import routers

from courses.api.v1 import views

router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)
router.register('lectures', views.LectureViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('courses/<int:pk>/participants/', views.ParticipantView.as_view()),
    path('courses/<int:pk>/lectures/', views.AvaibleLectureListView.as_view()),
    path('tasks/<int:pk>/solutions/', views.CompletedSolutionListView.as_view()),
    path('lectures/<int:pk>/tasks/', views.AvaibleTaskListView.as_view()),
    path('solutions/<int:pk>/marks/', views.SolutionMarkView.as_view()),
    path('tasks/', views.TaskView.as_view()),
    path('solutions/', views.SolutionView.as_view()),
    path('marks/<int:pk>/', views.MarkView.as_view()),
    path('marks/', views.MarkView.as_view()),
    path('comments/', views.CommentView.as_view()),
    path('marks/<int:pk>/comments/', views.CommentView.as_view()),
]
