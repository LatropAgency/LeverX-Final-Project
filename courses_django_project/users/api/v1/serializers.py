from rest_framework import serializers

from users.models import User


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
