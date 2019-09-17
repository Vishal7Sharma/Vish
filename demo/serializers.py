from rest_framework import serializers
from demo.models import Blog
from django.contrib.auth.models import User

"""Serializing Django objects. 
Django's serialization framework provides a mechanism for “translating” Django models into other formats.
Usually these other formats will be text-based and used for sending Django data over a wire,
but it's possible for a serializer to handle any format (text-based or not)."""


class BlogSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    content = serializers.CharField(required=False, allow_blank=True, max_length=400)

    def create(self, validated_data):
        """create and return a serializer new Blog instance, given the validated data"""
        return Blog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """update and return the existing Blog instance, given the validate data """
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)

        instance.save()
        return instance


class BlogModelSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'author', ]


class UserSerializer(serializers.ModelSerializer):
    # posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Blog.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', ]
