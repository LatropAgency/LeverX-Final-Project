from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.api.v1.serializers import UserSerializer


class UserView(generics.CreateAPIView):
    """
    Creates a user instance
    """
    permission_classes = [~IsAuthenticated]
    serializer_class = UserSerializer
