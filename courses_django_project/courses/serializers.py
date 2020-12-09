from rest_framework import serializers

from users.models import User
from courses.models import Course, Lecture, Task, Solution, Mark, Comment


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'role')
        extra_kwargs = {
            'password': {'write_only': True},
        }


class CourseSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'participants')


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ('id', 'course', 'topic', 'document')


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


class SuccessSerializer(serializers.Serializer):
    success = serializers.BooleanField(initial=True)

    class Meta:
        fields = ('success',)
        read_only_fields = ('success',)


class ErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()

    class Meta:
        fields = ('detail',)
