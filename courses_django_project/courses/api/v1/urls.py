from django.urls import path, include

from rest_framework_nested import routers

from courses.api.v1 import views

router = routers.SimpleRouter()
router.register('courses', views.CourseViewSet)
course_router = routers.NestedSimpleRouter(router, 'courses', lookup='course')
course_router.register('lectures', views.LectureViewSet, basename='lectures')
course_router.register('participants', views.ParticipantViewSet, basename='participant')
lecture_router = routers.NestedSimpleRouter(course_router, 'lectures', lookup='lecture')
lecture_router.register('tasks', views.TaskViewSet, basename='tasks')
task_router = routers.NestedSimpleRouter(lecture_router, 'tasks', lookup='task')
task_router.register('solutions', views.SolutionViewSet, basename='solutions')
solution_router = routers.NestedSimpleRouter(task_router, 'solutions', lookup='solution')
solution_router.register('marks', views.MarkViewSet, basename='marks')
mark_router = routers.NestedSimpleRouter(solution_router, 'marks', lookup='mark')
mark_router.register('comments', views.CommentViewSet, basename='comments')

app_name = 'course'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(course_router.urls)),
    path('', include(lecture_router.urls)),
    path('', include(task_router.urls)),
    path('', include(solution_router.urls)),
    path('', include(mark_router.urls)),
]
