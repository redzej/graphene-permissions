from .permissions import AllowAny
from django.core.exceptions import PermissionDenied
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoConnectionField


PERMISSION_DENIED_MSG = 'Permission Denied'


class AuthNode:
    permission_classes = (AllowAny, )

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
            raise PermissionDenied(PERMISSION_DENIED_MSG)


class AuthMutation:
    permission_classes = (AllowAny, )

    @classmethod
    def has_permission(cls, input, context, info):
        if not all([perm() for perm in cls.permission_classes]):
            raise PermissionDenied(PERMISSION_DENIED_MSG)


class AuthFilter(DjangoFilterConnectionField):
    """
    Custom ConnectionField for basic authentication system.
    """
    permission_classes = (AllowAny, )

    @classmethod
    def has_permission(cls, context):
        return all([permission() for permission in cls.permission_classes])

    def connection_resolver(cls, resolver, connection, default_manager, max_limit,
                            enforce_first_or_last, filterset_class, filtering_args,
                            root, args, context, info):

        if not cls.has_permission(context):
            return DjangoConnectionField.connection_resolver(
                resolver, connection, (PermissionDenied(PERMISSION_DENIED_MSG), ),
                max_limit, enforce_first_or_last, root, args, context, info,
            )

        return super().connection_resolver(
            resolver, connection, default_manager, max_limit, enforce_first_or_last,
            filterset_class, filtering_args, root, args, context, info,
        )
