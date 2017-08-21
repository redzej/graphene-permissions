class AllowAny:
    """
    Default authentication class.
    Allows any user for any action.
    """
    def has_node_permission(self, id, context, info):
        return True

    def has_mutation_permission(self, input, context, info):
        return True

    def has_filter_permission(self, context):
        return True


class AllowAuthenticated:
    """
    Base authentication class.
    Allows performing action only for logged in users.
    """

    def has_node_permisison(self, id, context, info):
        if hasattr(context, 'user'):
            return context.user and context.user.is_authenticated()
        return False

    def has_mutation_permission(self, input, context, info):
        if hasattr(context, 'user'):
            return context.user and context.user.is_authenticated()
        return False

    def has_filter_permission(self, context):
        if hasattr(context, 'user'):
            return context.user and context.user.is_authenticated()
        return False


class AllowStaff(AllowAuthenticated):
    """
    Base authentication class.
    Allow performing action only for admin and staff users.
    """

    def has_node_permisison(self, id, context, info):
        return super().has_node_permisison(id, context, info) and context.user.is_staff()

    def has_mutation_permission(self, input, context, info):
        return super().has_mutation_permission(input, context, info) and context.user.is_staff()

    def has_filter_permission(self, context):
        return super().has_filter_permission(context) and context.user.is_staff()
