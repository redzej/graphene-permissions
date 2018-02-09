class AllowAny:
    """
    Default authentication class.
    Allows any user for any action.
    Subclass it and override methods below.
    """

    @staticmethod
    def has_node_permission(info, id):
        return True

    @staticmethod
    def has_mutation_permission(root, info, input):
        return True

    @staticmethod
    def has_filter_permission(info):
        return True


class AllowAuthenticated:
    """
    Allows performing action only for logged in users.
    """

    @staticmethod
    def has_node_permission(info, id):
        return info.context.user.is_authenticated

    @staticmethod
    def has_mutation_permission(root, info, input):
        return info.context.user.is_authenticated

    @staticmethod
    def has_filter_permission(info):
        return info.context.user.is_authenticated


class AllowStaff:
    """
    Allow performing action only for staff users.
    """

    @staticmethod
    def has_node_permission(info, id):
        return info.context.user.is_staff

    @staticmethod
    def has_mutation_permission(root, info, input):
        return info.context.user.is_staff

    @staticmethod
    def has_filter_permission(info):
        return info.context.user.is_staff
