from functools import partial
from typing import Any, Optional

from django.db.models import Model
from graphene import ResolveInfo
from graphene_django.filter import DjangoFilterConnectionField

from graphene_permissions.permissions import AllowAny


class AuthNode:
    """
    Permission mixin for queries (nodes).
    Allows for simple configuration of access to nodes via class system.
    """

    permission_classes = (AllowAny,)

    @classmethod
    def get_node(cls, info: ResolveInfo, id: str) -> Optional[Model]:
        if all((perm.has_node_permission(info, id) for perm in cls.permission_classes)):
            try:
                object_instance = cls._meta.model.objects.get(pk=id)  # type: ignore
            except cls._meta.model.DoesNotExist:  # type: ignore
                object_instance = None
            return object_instance
        else:
            return None


class AuthMutation:
    """
    Permission mixin for ClientIdMutation.
    """

    permission_classes = (AllowAny,)

    @classmethod
    def has_permission(cls, root: Any, info: ResolveInfo, input: dict) -> bool:
        return all(
            (
                perm.has_mutation_permission(root, info, input)
                for perm in cls.permission_classes
            )
        )


class AuthFilter(DjangoFilterConnectionField):
    """
    Custom ConnectionField for permission system.
    """

    permission_classes = (AllowAny,)

    @classmethod
    def has_permission(cls, info: ResolveInfo) -> bool:
        return all(
            (perm.has_filter_permission(info) for perm in cls.permission_classes)
        )

    @classmethod
    def connection_resolver(
        cls,
        resolver,
        connection,
        default_manager,
        queryset_resolver,
        max_limit,
        enforce_first_or_last,
        root,
        info,
        **args
    ):
        if not cls.has_permission(info):
            on_resolve = partial(cls.resolve_connection, connection, args)
            return on_resolve([])

        return super(DjangoFilterConnectionField, cls).connection_resolver(
            resolver,
            connection,
            default_manager,
            queryset_resolver,
            max_limit,
            enforce_first_or_last,
            root,
            info,
            **args,
        )
