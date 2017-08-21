class AllowAny:
    """Base authentication class."""
    def has_node_permission(self):
        return True

    def has_mutation_permission(self):
        return True

    def has_filter_permission(self):
        return True
