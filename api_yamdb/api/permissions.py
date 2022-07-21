from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS, BasePermission
from django.db.models import Q


class IsAdminOrReadOnly(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        user = request.user
        is_admin = User.objects.filter(
            Q(role__in=('admin', 'superuser')) & Q(id=user.id)
        ).exists()
        return is_admin


class OwherAdminOrReadOnly(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        user = request.user
        return True if (user.role in ('admin', 'moderator', 'superuser') or user == obj.author) else False
