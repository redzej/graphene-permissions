class AllowAny:
    """
    Default authentication class.
    Allows any user for any action.
    Subclass it and override methods below.
    """
    def has_node_permission(self, id, context, info):
        return True

    def has_mutation_permission(self, input, context, info):
        return True

    def has_filter_permission(self, context):
        return True


class AllowAuthenticated:
    """
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


class AllowStaff:
    """
    Allow performing action only for staff users.
    """

    def has_node_permisison(self, id, context, info):
        return context.user.is_staff()

    def has_mutation_permission(self, input, context, info):
        return context.user.is_staff()

    def has_filter_permission(self, context):
        return context.user.is_staff()
