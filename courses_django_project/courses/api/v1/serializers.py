from rest_framework import serializers

from courses.models import (
    Solution,
    Lecture,
    Comment,
    Course,
    Mark,
    Task,
)

from users.api.v1.serializers import UserSerializer


class CourseSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'participants')


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ('id', 'topic', 'document')


class ParticipantSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    class Meta:
        fields = ('id',)
        read_only_fields = ('id',)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'lecture', 'text')


class SolutionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Solution
        fields = ('id', 'task', 'user', 'text')


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ('id', 'solution', 'result')


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'mark', 'user', 'text')
