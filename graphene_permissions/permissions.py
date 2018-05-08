from typing import Any

from graphql import ResolveInfo


class AllowAny:
    """
    Default authentication class.
    Allows any user for any action.
    Subclass it and override methods below.
    """

    @staticmethod
    def has_node_permission(info: ResolveInfo, id: str) -> bool:
        return True

    @staticmethod
    def has_mutation_permission(root: Any, info: ResolveInfo, input: dict) -> bool:
        return True

    @staticmethod
    def has_filter_permission(info: ResolveInfo) -> bool:
        return True


class AllowAuthenticated:
    """
    Allows performing action only for logged in users.
    """

    @staticmethod
    def has_node_permission(info: ResolveInfo, id: str) -> bool:
        return info.context.user.is_authenticated

    @staticmethod
    def has_mutation_permission(root: Any, info: ResolveInfo, input: dict) -> bool:
        return info.context.user.is_authenticated

    @staticmethod
    def has_filter_permission(info: ResolveInfo) -> bool:
        return info.context.user.is_authenticated


class AllowStaff:
    """
    Allow performing action only for staff users.
    """

    @staticmethod
    def has_node_permission(info: ResolveInfo, id: str) -> bool:
        return info.context.user.is_staff

    @staticmethod
    def has_mutation_permission(root: Any, info: ResolveInfo, input: dict) -> bool:
        return info.context.user.is_staff

    @staticmethod
    def has_filter_permission(info: ResolveInfo) -> bool:
        return info.context.user.is_staff


class AllowSuperuser:
    """
    Allow performing action only for superusers.
    """

    @staticmethod
    def has_node_permission(info: ResolveInfo, id: str) -> bool:
        return info.context.user.is_superuser

    @staticmethod
    def has_mutation_permission(root: Any, info: ResolveInfo, input: dict) -> bool:
        return info.context.user.is_superuser

    @staticmethod
    def has_filter_permission(info: ResolveInfo) -> bool:
        return info.context.user.is_superuser
