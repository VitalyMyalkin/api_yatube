from rest_framework import serializers

from posts.models import Post, Comment, Group


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    post = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
