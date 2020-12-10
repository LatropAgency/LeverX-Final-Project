from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, mixins
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.error_serializer import ErrorSerializer
from core.success_serializer import SuccessSerializer
from core.permissions import (
    StudentOrTeacherReadOnly,
    TeacherOrStudentReadOnly,
    IsParticipant,
    TeacherOnly,
)

from users.models import User
from users.enum_types import RoleTypes

from courses.api.v1.serializers import (
    SolutionSerializer,
    CommentSerializer,
    TaskSerializer,
    MarkSerializer,
)
from courses.models import Course, Lecture, Task, Solution, Mark, Comment
from courses.api.v1.serializers import CourseSerializer, LectureSerializer, ParticipantSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    Create, retrieve, update, delete a course instance
    """
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated & TeacherOrStudentReadOnly]
    serializer_class = CourseSerializer

    def get_queryset(self):
        return self.queryset.filter(participants__in=[self.request.user])


class LectureViewSet(viewsets.ModelViewSet):
    """
    Create, retrieve, update, delete a lecture instance
    """
    parser_classes = (MultiPartParser, FormParser)
    queryset = Lecture.objects.all()
    permission_classes = [IsAuthenticated & TeacherOrStudentReadOnly & IsParticipant]
    serializer_class = LectureSerializer

    def get_queryset(self):
        return self.queryset.filter(course__id=self.kwargs['course_pk'])

    def perform_create(self, serializer):
        serializer.save(course_id=self.kwargs['course_pk'])

    def perform_update(self, serializer):
        serializer.save(course_id=self.kwargs['course_pk'])


class TaskViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """
    Create, list, retrieve a task instance
    """
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated & TeacherOrStudentReadOnly & IsParticipant]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return self.queryset.filter(lecture__id=self.kwargs['lecture_pk'],
                                    lecture__course__id=self.kwargs['course_pk'])

    def post(self, request, *args, **kwargs):
        return self.create(self, request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(lecture_id=self.kwargs['lecture_pk'])


class ParticipantViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    """
    Create, delete a participant instance
    """
    permission_classes = [IsAuthenticated & TeacherOnly & IsParticipant]
    serializer_class = ParticipantSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = ParticipantSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, pk=serializer.data['id'])
            course = Course.objects.get(pk=kwargs['course_pk'])
            if user not in course.participants.all():
                course.participants.add(user)
                course.save()
            else:
                return Response(ErrorSerializer({'detail': "This user has already joined"}).data,
                                status=status.HTTP_403_FORBIDDEN)
            return Response(SuccessSerializer().data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        serializer = ParticipantSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, pk=serializer.data['id'])
            if user.role == RoleTypes.TEACHER.value:
                return Response(ErrorSerializer({'detail': "You can't remove teacher"}).data,
                                status=status.HTTP_403_FORBIDDEN)
            course = Course.objects.get(pk=kwargs['course_pk'])
            if user not in course.participants.all():
                raise Http404
            course.participants.remove(user)
            return Response(SuccessSerializer().data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SolutionViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    """
    Create, list, retrieve a solution instance
    """
    queryset = Solution.objects.all()
    permission_classes = [IsAuthenticated & StudentOrTeacherReadOnly & IsParticipant]
    serializer_class = SolutionSerializer

    def get_queryset(self):
        if self.request.user.role == RoleTypes.STUDENT.value:
            return self.queryset.filter(task__id=self.kwargs['task_pk'], user__id=self.request.user.id,
                                        task__lecture__id=self.kwargs['lecture_pk'],
                                        task__lecture__course__id=self.kwargs['course_pk'])
        return self.queryset.filter(task__id=self.kwargs['task_pk'],
                                    task__lecture__id=self.kwargs['lecture_pk'],
                                    task__lecture__course__id=self.kwargs['course_pk'])

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(task_id=self.kwargs['task_pk'], user_id=self.request.user.id)


class MarkViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Create, retrieve, update a mark instance
    """
    queryset = Mark.objects.all()
    permission_classes = [IsAuthenticated & TeacherOrStudentReadOnly & IsParticipant]
    serializer_class = MarkSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(solution_id=self.kwargs['solution_pk'])


class CommentViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    """
    Create, list a comment instance
    """
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated & IsParticipant]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return self.queryset.filter(mark__id=self.kwargs['mark_pk'],
                                    mark__solution__id=self.kwargs['solution_pk'],
                                    mark__solution__task__id=self.kwargs['task_pk'],
                                    mark__solution__task__lecture__id=self.kwargs['lecture_pk'],
                                    mark__solution__task__lecture__course__id=self.kwargs['course_pk'])

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(mark_id=self.kwargs['mark_pk'], user_id=self.request.user.id)
