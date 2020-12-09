from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, generics, mixins
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from core.permissions import TeacherOrStudentReadOnly, TeacherOnly, StudentOrTeacherReadOnly, StudentOnly, IsParticipant

from users.models import User
from users.enum_types import RoleTypes

from courses.serializers import UserSerializer, TaskSerializer, SolutionSerializer, MarkSerializer, CommentSerializer, \
    SuccessSerializer, ErrorSerializer
from courses.models import Course, Lecture, Task, Solution, Mark, Comment
from courses.serializers import CourseSerializer, LectureSerializer, ParticipantSerializer


class UserList(mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = [~IsAuthenticated]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated & TeacherOrStudentReadOnly & IsParticipant]
    serializer_class = CourseSerializer

    def get_queryset(self):
        return self.queryset.filter(participants__in=[self.request.user])

    def create(self, request, *args, **kwargs):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            course = Course.objects.create(**serializer.data)
            course.participants.add(request.user)
            course.save()
            return Response(CourseSerializer(course).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LectureViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)
    queryset = Lecture.objects.all()
    permission_classes = [IsAuthenticated & TeacherOnly & IsParticipant]
    serializer_class = LectureSerializer

    def get_queryset(self):
        return self.queryset.filter(course__participants__in=[self.request.user])


class TaskView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated & TeacherOnly]
    serializer_class = TaskSerializer


class ParticipantView(APIView):
    permission_classes = [IsAuthenticated & TeacherOnly]

    def post(self, request, pk):
        serializer = ParticipantSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, pk=serializer.data['id'])
            course = get_object_or_404(Course, pk=pk)
            if user not in course.participants.all():
                course.participants.add(user)
                course.save()
            else:
                return Response(ErrorSerializer({'detail': "This user has already joined"}).data,
                                status=status.HTTP_403_FORBIDDEN)
            return Response(SuccessSerializer().data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, pk):
        serializer = ParticipantSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, pk=serializer.data['id'])
            if user.role == RoleTypes.TEACHER.value:
                return Response(ErrorSerializer({'detail': "You can't remove teacher"}).data,
                                status=status.HTTP_403_FORBIDDEN)
            course = get_object_or_404(Course, pk=pk)
            if user not in course.participants.all():
                raise Http404
            course.participants.remove(user)
            return Response(SuccessSerializer().data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SolutionView(generics.ListCreateAPIView):
    queryset = Solution.objects.all()
    permission_classes = [IsAuthenticated & StudentOnly]
    serializer_class = SolutionSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = SolutionSerializer(data=request.data)
        if serializer.is_valid():
            task = get_object_or_404(Task, id=serializer.data['task'])
            solution = Solution.objects.create(user=request.user, task=task, text=serializer.data['text'])
            return Response(SolutionSerializer(solution).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MarkView(mixins.UpdateModelMixin, generics.ListCreateAPIView):
    queryset = Mark.objects.all()
    permission_classes = [IsAuthenticated & TeacherOrStudentReadOnly]
    serializer_class = MarkSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class CommentView(mixins.RetrieveModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        comments = Comment.objects.filter(mark_id=kwargs['pk'])
        return Response(CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            mark = get_object_or_404(Mark, id=serializer.data['mark'])
            comment = Comment.objects.create(user=request.user, mark=mark, text=serializer.data['text'])
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompletedSolutionListView(APIView):
    permission_classes = [IsAuthenticated & TeacherOnly]

    def get(self, request, pk):
        solutions = Solution.objects.filter(task__pk=pk)
        return Response(SolutionSerializer(solutions, many=True).data, status=status.HTTP_200_OK)


class AvaibleLectureListView(APIView):
    permission_classes = [IsAuthenticated & StudentOnly]

    def get(self, request, pk):
        lectures = Lecture.objects.filter(course__pk=pk)
        return Response(LectureSerializer(lectures, many=True).data, status=status.HTTP_200_OK)


class AvaibleTaskListView(APIView):
    permission_classes = [IsAuthenticated & StudentOnly]

    def get(self, request, pk):
        tasks = Task.objects.filter(lecture__pk=pk)
        return Response(TaskSerializer(tasks, many=True).data, status=status.HTTP_200_OK)


class SolutionMarkView(APIView):
    permission_classes = [IsAuthenticated & StudentOnly]

    def get(self, request, pk):
        marks = Mark.objects.filter(solution__pk=pk)
        return Response(MarkSerializer(marks, many=True).data, status=status.HTTP_200_OK)
