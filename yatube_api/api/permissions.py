from rest_framework import permissions


class PostPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        # здесь проверка запроса на SAFE.METHODS не годится: по условиям
        # задачи ответы могут уходить только авторизованным пользователям,
        # иначе мы тесты не проходим
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
