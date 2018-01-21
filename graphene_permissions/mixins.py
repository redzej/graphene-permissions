from graphene_django.filter import DjangoFilterConnectionField
from graphene_permissions.permissions import AllowAny


def deny_permission():
    return None


class AuthNode:
    permission_classes = (AllowAny,)
    permission_denied = deny_permission

    @classmethod
    def get_node(cls, info, id):

        def has_permission():
            return all([perm().has_node_permission(info, id) for perm in cls.permission_classes])

        if has_permission():
            try:
                object_instance = cls._meta.model.objects.get(id=id)
            except cls._meta.model.DoesNotExist:
                object_instance = None
            return object_instance
        else:
            cls.permission_denied()


class AuthMutation:
    permission_classes = (AllowAny,)
    permission_denied = deny_permission

    @classmethod
    def has_permission(cls, input, info):
        if not all([perm().has_mutation_permission(input, info) for perm in cls.permission_classes]):
            cls.permission_denied()


class AuthFilter(DjangoFilterConnectionField):
    """
    Custom ConnectionField for basic authentication system.
    """
    permission_classes = (AllowAny,)
    permission_denied = deny_permission

    @classmethod
    def has_permission(cls, info):
        return all([permission() for permission in cls.permission_classes])

    @classmethod
    def connection_resolver(
            cls, resolver, connection, default_manager, max_limit,
            enforce_first_or_last, filterset_class, filtering_args,
            root, info, **args
    ):
        if not cls.has_permission(info):
            return super().connection_resolver(
                resolver, connection, cls.permission_denied(),
                max_limit, enforce_first_or_last, root, info, **args
            )

        return super().connection_resolver(
            resolver, connection, default_manager, max_limit, enforce_first_or_last,
            filterset_class, filtering_args, root, info, **args,
        )