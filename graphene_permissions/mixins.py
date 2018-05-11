from typing import Any, Optional

from django.db.models import Model
from graphene_django.filter import DjangoFilterConnectionField
from graphql import ResolveInfo

from graphene_permissions.permissions import AllowAny


class AuthNode:
    """
    Permission mixin for queries (nodes).
    Allows for simple configuration of access to nodes via class system.
    """
    permission_classes = (AllowAny,)

    @classmethod
    def get_node(cls, info: ResolveInfo, id: str) -> Optional[Model]:
        if all((perm().has_node_permission(info, id) for perm in cls.permission_classes)):
            try:
                object_instance = cls._meta.model.objects.get(id=id)  # type: ignore
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
            (perm().has_mutation_permission(root, info, input) for perm in cls.permission_classes)
        )


class AuthFilter(DjangoFilterConnectionField):
    """
    Custom ConnectionField for permission system.
    """
    permission_classes = (AllowAny,)

    @classmethod
    def has_permission(cls, info: ResolveInfo) -> bool:
        return all(
            (perm().has_filter_permission(info) for perm in cls.permission_classes)
        )

    @classmethod
    def connection_resolver(
            cls, resolver, connection, default_manager,
            max_limit, enforce_first_or_last, filterset_class,
            filtering_args, root, info, **args
    ):

        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        qs = filterset_class(
            data=filter_kwargs,
            queryset=default_manager.get_queryset()
        ).qs

        if not cls.has_permission(info):
            return super(DjangoFilterConnectionField, cls).connection_resolver(
                resolver, connection, qs.none(), max_limit, enforce_first_or_last,
                root, info, **args,
            )

        return super(DjangoFilterConnectionField, cls).connection_resolver(
            resolver, connection, qs, max_limit, enforce_first_or_last,
            filterset_class, filtering_args, **args,
        )
