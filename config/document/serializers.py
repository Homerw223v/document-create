from rest_framework import serializers


class DocumentSerializer(serializers.Serializer):
    """Serializer for name and data from input."""

    name = serializers.CharField()
    data = serializers.CharField()
