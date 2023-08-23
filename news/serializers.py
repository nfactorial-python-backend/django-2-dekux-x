from rest_framework import serializers

class NewsSersializer(serializers.Serializer):
    title = serializers.CharField(max_length = 200)
    content = serializers.CharField()
