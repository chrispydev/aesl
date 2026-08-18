from rest_framework import serializers


class SearchResultSerializer(serializers.Serializer):

    type = serializers.CharField()

    name = serializers.CharField()

    rank = serializers.CharField(
        required=False,
        allow_blank=True
    )

    url = serializers.CharField()
