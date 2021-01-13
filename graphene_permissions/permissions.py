import operator
from typing import Any

from graphql import ResolveInfo


class BaseOperatorPerm:
    def __init__(self, op1: Any, op2: Any):
        self.op1 = op1
        self.op2 = op2

    def __call__(self):
        return self

    def has_permission(self, info: ResolveInfo):
        return self.op_func(
            self.op1.has_permission(info), self.op2.has_permission(info)
        )

    def has_node_permission(self, info: ResolveInfo, id: str) -> bool:
        return self.op_func(
            self.op1.has_node_permission(info, id),
            self.op2.has_node_permission(info, id),
        )

    def has_mutation_permission(
        self, root: Any, info: ResolveInfo, input: dict
    ) -> bool:
        return self.op_func(
            self.op1.has_mutation_permission(root, info, input),
            self.op2.has_mutation_permission(root, info, input),
        )

    def has_filter_permission(self, info: ResolveInfo):
        return self.op_func(
            self.op1.has_filter_permission(info), self.op2.has_filter_permission(info)
        )


class BaseSingleOperatorPerm(BaseOperatorPerm):
    def __init__(self, op1: Any):
        self.op1 = op1

    def has_permission(self, info: ResolveInfo):
        return self.op_func(self.op1.has_permission(info))

    def has_node_permission(self, info: ResolveInfo, id: str) -> bool:
        return self.op_func(self.op1.has_node_permission(info, id))

    def has_mutation_permission(
        self, root: Any, info: ResolveInfo, input: dict
    ) -> bool:
        return self.op_func(self.op1.has_mutation_permission(root, info, input))

    def has_filter_permission(self, info: ResolveInfo):
        return self.op_func(self.op1.has_filter_permission(info))


class AND(BaseOperatorPerm):
    op_func = operator.and_

    def __repr__(self):
        return f"({self.op1} AND {self.op2})"


class OR(BaseOperatorPerm):
    op_func = operator.or_

    def __repr__(self):
        return f"({self.op1} OR {self.op2})"


class NOT(BaseSingleOperatorPerm):
    op_func = operator.not_

    def __repr__(self):
        return f"(NOT {self.op1})"


class BasePermissionMetaclass(type):
    def __and__(self, other):
        return AND(self, other)

    def __or__(self, other):
        return OR(self, other)

    def __rand__(self, other):
        return AND(other, self)

    def __ror__(self, other):
        return OR(other, self)

    def __invert__(self):
        return NOT(self)


class BasePermission(metaclass=BasePermissionMetaclass):
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
