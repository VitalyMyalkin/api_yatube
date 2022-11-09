from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from posts.models import Post, Comment, Group
from .serializers import PostSerializer, CommentSerializer, GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        if serializer.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostViewSet, self).perform_destroy(serializer)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@api_view(['GET', 'POST'])
def api_comments(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    comments = post.comments.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_comments_detail(request, pk, id):
    post = get_object_or_404(Post, id=pk)
    comment = get_object_or_404(Comment, id=id)
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if not request.user == comment.author:
        return Response(status=status.HTTP_403_FORBIDDEN)
    # если пользователь, обратившийся к API, не является автором коммента,
    # то к методам, идущим после GET, мы его не пропускаем
    # и возвращаем ответ со статусом 403

    if request.method == 'PUT' or request.method == 'PATCH':
        serializer = CommentSerializer(comment,
                                       data=request.data,
                                       partial=True
                                       )
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
