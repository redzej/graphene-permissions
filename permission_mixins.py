from .permission_classes import AllowAny, AllowAuthenticated, AllowStaff


class AuthNodeMixin:
    permission_class = (AllowAny, )

    @classmethod
    def get_node(cls, id, context, info):

        def has_permission():
            pass

        if has_permission():
            pass

        pass


class AuthMutationMixin:
    permission_class = (AllowAny, )

    @classmethod
    def has_permission(cls, input, context, info):
        pass
