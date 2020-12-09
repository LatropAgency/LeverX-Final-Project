from rest_framework import serializers


class SuccessSerializer(serializers.Serializer):
    success = serializers.BooleanField(initial=True)

    class Meta:
        fields = ('success',)
        read_only_fields = ('success',)
