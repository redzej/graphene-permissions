from django.core.exceptions import PermissionDenied
from graphene_django import DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField

from .permissions import AllowAny

PERMISSION_DENIED_MSG = 'Permission Denied'


def access_denied_resolver():
    return None


class AuthNode:
    permission_classes = (AllowAny, )
    deny_resolver = access_denied_resolver

    @classmethod
    def get_node(cls, id, context, info):

        def has_permission():
            return all([perm() for perm in cls.permission_classes])

        if has_permission():
            try:
                object_instance = cls._meta.model.objects.get(id=id)
            except cls._meta.model.DoesNotExist:
                object_instance = None

            return object_instance

        else:
            cls.deny_resolver()


class AuthMutation:
    permission_classes = (AllowAny, )
    deny_resolver = access_denied_resolver

    @classmethod
    def has_permission(cls, input, context, info):
        if not all([perm() for perm in cls.permission_classes]):
            cls.deny_resolver()


class AuthFilter(DjangoFilterConnectionField):
    """
    Custom ConnectionField for basic authentication system.
    """
    permission_classes = (AllowAny, )
    deny_resolver = access_denied_resolver

    @classmethod
    def has_permission(cls, context):
        return all([permission() for permission in cls.permission_classes])

    def connection_resolver(cls, resolver, connection, default_manager, max_limit,
                            enforce_first_or_last, filterset_class, filtering_args,
                            root, info, **args):

        if not cls.has_permission(info.context):
            return DjangoConnectionField.connection_resolver(
                resolver, connection, qs, max_limit, enforce_first_or_last,
                root, info, **args
            )

        return super().connection_resolver(
            resolver, connection, default_manager, max_limit, enforce_first_or_last,
            filterset_class, filtering_args, root, args, context, info,
        )
