from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticated

from users.api.v1.serializers import UserSerializer


class UserView(mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = [~IsAuthenticated]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
