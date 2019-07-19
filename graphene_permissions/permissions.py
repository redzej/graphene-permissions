from typing import Any

from graphql import ResolveInfo


class BasePermission:
    """
    Base permission class.
    Subclass it and override methods below.
    """

    @classmethod
    def has_permission(cls, info: ResolveInfo) -> bool:
        """Fallback for other has_..._permission functions.
        Returns False by default, overwrite for custom behaviour.
        """
        return False

    @classmethod
    def has_node_permission(cls, info: ResolveInfo, id: str) -> bool:
        return cls.has_permission(info)

    @classmethod
    def has_mutation_permission(cls, root: Any, info: ResolveInfo, input: dict) -> bool:
        return cls.has_permission(info)

    @classmethod
    def has_filter_permission(cls, info: ResolveInfo) -> bool:
        return cls.has_permission(info)


class AllowAny(BasePermission):
    """
    Default authentication class.
    Allows any user for any action.
    """

    @classmethod
    def has_permission(cls, info: ResolveInfo) -> bool:
        return True


class AllowAuthenticated(BasePermission):
    """
    Allows performing action only for logged in users.
    """

    @classmethod
    def has_permission(cls, info: ResolveInfo) -> bool:
        return info.context.user.is_authenticated


class AllowStaff(BasePermission):
    """
    Allow performing action only for staff users.
    """

    @classmethod
    def has_permission(cls, info: ResolveInfo) -> bool:
        return info.context.user.is_staff


class AllowSuperuser(BasePermission):
    """
    Allow performing action only for superusers.
    """

    @classmethod
    def has_permission(cls, info: ResolveInfo) -> bool:
        return info.context.user.is_superuser
